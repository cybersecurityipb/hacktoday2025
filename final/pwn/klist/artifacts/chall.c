#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/module.h>
#include <linux/uio.h>
#include <linux/version.h>
#include <linux/types.h>
#include <linux/ioctl.h>

#define DEVICE_NAME "klist"
#define DATA_SZ 0x60
#define MAX_NODE 10

struct klist_entry {
	char data[DATA_SZ];
    struct klist_entry *next;
	size_t pos;
};

struct klist_fd {
    struct klist_entry *head;
    size_t max_index;
    size_t count;        /* <--- added: how many nodes currently in list */
    struct mutex lock;   /* <--- added: protect per-FD list ops */
};

/* userspace-visible helper structs (kernel side) */

struct add_req {
    char buf[DATA_SZ];       /* data to add to list */
};

struct edit_req {
    uint32_t idx;            /* index of node to edit */
	uint32_t sz;			/* how much data copied */
    char buf[DATA_SZ];       /* data to append/overwrite from pos */
};

struct show_req {
    uint32_t idx;            /* index of node to show */
    char buf[DATA_SZ];       /* out: kernel will fill this and copy back */
};


#define KLIST_IOCTL_ADD  _IOW('k', 0, struct add_req)
#define KLIST_IOCTL_EDIT _IOW('k', 1, struct edit_req)
#define KLIST_IOCTL_SHOW _IOWR('k', 2, struct show_req)

static int klist_open(struct inode *inode, struct file *file)
{
    struct klist_fd *st = kzalloc(sizeof(*st), GFP_KERNEL);
    if (!st)
        return -ENOMEM;

    st->head = NULL;
    st->max_index = MAX_NODE;
    st->count = 0;
    mutex_init(&st->lock);        /* initialise mutex */
    file->private_data = st;

    pr_info("klist: opened fd %px\n", file);
    return 0;
}

static int klist_release(struct inode *inode, struct file *file)
{
    struct klist_fd *st = file->private_data;
    struct klist_entry *n, *tmp;

    if (!st)
        return 0;

    /* free the linked list owned by this fd */
    n = st->head;
    while (n) {
        tmp = n->next;
        kfree(n);
        n = tmp;
    }

    kfree(st);
    file->private_data = NULL;
    pr_info("klist: released fd %px\n", file);
    return 0;
}

static long klist_ioctl(struct file *file, unsigned int command, unsigned long arg)
{
    struct klist_fd *st = file->private_data;

    if (!st)
        return -EBADFD;

    switch (command) {
    case KLIST_IOCTL_ADD: {
        struct klist_entry *node;
        char tmp[DATA_SZ];

        /* capacity check */
        if (st->count >= st->max_index)
            return -ENOSPC;

        /* copy from userspace (up to DATA_SZ bytes) */
        if (copy_from_user(tmp, (char __user *)arg, DATA_SZ))
            return -EFAULT;

        /* allocate */
        node = kzalloc(sizeof(*node), GFP_KERNEL);
        if (!node)
            return -ENOMEM;

        /* init node */
        memcpy(node->data, tmp, DATA_SZ);
        node->pos = strnlen(node->data, DATA_SZ); /* initial pos = length if user nul-terminated, else DATA_SZ */
        node->next = NULL;

        /* append to per-FD list (under lock) */
        mutex_lock(&st->lock);
        if (!st->head) {
            st->head = node;
        } else {
            struct klist_entry *cur = st->head;
            while (cur->next)
                cur = cur->next;
            cur->next = node;
        }
        st->count++;
        mutex_unlock(&st->lock);

        pr_info("klist: added node@%px (count=%zu)\n", node, st->count);
        return 0;
    }

 	case KLIST_IOCTL_SHOW: {
		struct show_req sreq;
		struct klist_entry *cur;
		uint32_t target;
		size_t i;

		/* fetch the request (idx + userspace buffer to fill) */
		if (copy_from_user(&sreq, (void __user *)arg, sizeof(sreq)))
			return -EFAULT;

		target = sreq.idx;

		/* locate node */
		mutex_lock(&st->lock);
		cur = st->head;
		for (i = 0; i < target; i++) {
			if (!cur) {
				mutex_unlock(&st->lock);
				return -EINVAL;
			}
			cur = cur->next;
		}
		if (!cur) {
			mutex_unlock(&st->lock);
			return -EINVAL;
		}

		/* copy node data into sreq.buf; we copy exactly DATA_SZ bytes so userspace gets full slot */
		if (copy_to_user((void __user *)(((char __user *)arg) + offsetof(struct show_req, buf)),
						cur->data, DATA_SZ)) {
			mutex_unlock(&st->lock);
			return -EFAULT;
		}

		mutex_unlock(&st->lock);
		return 0;
	}

    case KLIST_IOCTL_EDIT: {
		struct edit_req ureq;
		struct klist_entry *cur;
		uint32_t target;
		size_t i;

		/* get request from userspace */
		if (copy_from_user(&ureq, (void __user *)arg, sizeof(ureq)))
			return -EFAULT;

		target = ureq.idx;

		if (ureq.sz > DATA_SZ || ureq.sz == 0) {
			mutex_unlock(&st->lock);
			return -EINVAL;
		}

		/* find node by index under lock */
		mutex_lock(&st->lock);
		cur = st->head;
		for (i = 0; i < target; i++) {
			if (!cur) {
				mutex_unlock(&st->lock);
				return -EINVAL;
			}
			cur = cur->next;
		}
		if (!cur) {
			mutex_unlock(&st->lock);
			return -EINVAL;
		}

		if (cur->pos >= DATA_SZ) {
			mutex_unlock(&st->lock);
			cur->pos = 0;
			return -ENOSPC;
		}

		memcpy(cur->data + cur->pos, ureq.buf, ureq.sz);
		cur->pos = strnlen(cur->data, DATA_SZ);

		pr_info("klist: EDIT node[%u] @%px pos=%zu next=%px\n",
				target, cur, cur->pos, cur->next);

		mutex_unlock(&st->lock);
		return 0;
	}


    default:
        return -EINVAL;
    }

    /* unreachable */
    return 0;
}


/* All the operations supported on this file */
static const struct file_operations klist_fops = {
	.owner = THIS_MODULE,
	.open = klist_open,
	.release = klist_release,
	.unlocked_ioctl = klist_ioctl
};


static dev_t device_region_start;
static struct class *device_class;
static struct cdev device;

/* Create the device class */
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 4, 0)
static inline struct class *klist_create_class(void) { return class_create(DEVICE_NAME); }
#else
static inline struct class *klist_create_class(void) { return class_create(THIS_MODULE, DEVICE_NAME); }
#endif

/* Make the device file accessible to normal users (rw-rw-rw-) */
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 2, 0)
static char *device_node(const struct device *dev, umode_t *mode) { if (mode) *mode = 0666; return NULL; }
#else
static char *device_node(struct device *dev, umode_t *mode) { if (mode) *mode = 0666; return NULL; }
#endif

/* Create the device when the module is loaded */
static int __init klist_module_init(void)
{
	int err;

	if ((err = alloc_chrdev_region(&device_region_start, 0, 1, DEVICE_NAME)))
		return err;

	err = -ENODEV;

	if (!(device_class = klist_create_class()))
		goto cleanup_region;
	device_class->devnode = device_node;

	if (!device_create(device_class, NULL, device_region_start, NULL, DEVICE_NAME))
		goto cleanup_class;

	cdev_init(&device, &klist_fops);
	if ((err = cdev_add(&device, device_region_start, 1)))
		goto cleanup_device;

	pr_info("Loaded /dev/%s\n", DEVICE_NAME);
	return 0;

cleanup_device:
	device_destroy(device_class, device_region_start);
cleanup_class:
	class_destroy(device_class);
cleanup_region:
	unregister_chrdev_region(device_region_start, 1);
	return err;
}

/* Destroy the device on exit */
static void __exit klist_module_exit(void)
{
	cdev_del(&device);
	device_destroy(device_class, device_region_start);
	class_destroy(device_class);
	unregister_chrdev_region(device_region_start, 1);

	pr_info("Unloaded /dev/%s\n", DEVICE_NAME);
}

module_init(klist_module_init);
module_exit(klist_module_exit);

MODULE_DESCRIPTION("/dev/" DEVICE_NAME ": a vulnerable kernel module");
MODULE_AUTHOR("yqroo <yqroo@hacktoday.web.id>");
MODULE_LICENSE("GPL");
