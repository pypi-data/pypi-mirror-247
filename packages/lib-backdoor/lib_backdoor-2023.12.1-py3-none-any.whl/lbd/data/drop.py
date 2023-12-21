def split_dataset(dataset, frac=0.1, perm: Union[np.ndarray, List[int], None] = None):
    perm = perm if perm else np.random.shuffle(np.arange(len(dataset)))
    nb_split = int(frac * len(dataset))
    # -------------------------
    lefted_set = deepcopy(dataset)
    lefted_set.data = lefted_set.data[perm[nb_split:]]
    lefted_set.targets = np.array(lefted_set.targets)[perm[nb_split:]].tolist()
    # -------------------------
    splited_set = deepcopy(dataset)
    splited_set.data = splited_set.data[perm[:nb_split]]
    splited_set.targets = np.array(splited_set.targets)[perm[:nb_split]].tolist()

    print(
        "total data size: %d images, split test size: %d images, split ratio: %f"
        % (len(lefted_set.targets), len(splited_set.targets), frac)
    )
    return splited_set, lefted_set


def get_train_loader(args):
    print("==> Preparing train data..")
    MEAN_CIFAR10 = (0.4914, 0.4822, 0.4465)
    STD_CIFAR10 = (0.2023, 0.1994, 0.2010)
    tf_train = transforms.Compose(
        [
            transforms.RandomCrop(32, padding=4),
            # transforms.RandomRotation(3),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(MEAN_CIFAR10, STD_CIFAR10),
        ]
    )

    if args.dataset == "CIFAR10":
        trainset = datasets.CIFAR10(root="data/CIFAR10", train=True, download=True)
    else:
        raise Exception("Invalid dataset")

    train_data = DatasetCL(args, full_dataset=trainset, transform=tf_train)
    train_loader = DataLoader(train_data, batch_size=args.batch_size, shuffle=True)

    return train_loader


def get_test_loader(args):
    print("==> Preparing test data..")
    MEAN_CIFAR10 = (0.4914, 0.4822, 0.4465)
    STD_CIFAR10 = (0.2023, 0.1994, 0.2010)
    tf_test = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize(MEAN_CIFAR10, STD_CIFAR10)]
    )
    if args.dataset == "CIFAR10":
        testset = datasets.CIFAR10(root="data/CIFAR10", train=False, download=True)
    else:
        raise Exception("Invalid dataset")

    test_data_clean = DatasetBD(
        args, full_dataset=testset, inject_portion=0, transform=tf_test, mode="test"
    )
    test_data_bad = DatasetBD(
        args, full_dataset=testset, inject_portion=1, transform=tf_test, mode="test"
    )

    # (apart from label 0) bad test data
    test_clean_loader = DataLoader(
        dataset=test_data_clean,
        batch_size=args.batch_size,
        shuffle=False,
    )
    # all clean test data
    test_bad_loader = DataLoader(
        dataset=test_data_bad,
        batch_size=args.batch_size,
        shuffle=False,
    )

    return test_clean_loader, test_bad_loader


def get_backdoor_loader(args):
    print("==> Preparing train data..")
    # tf_train = transforms.Compose([transforms.ToTensor()])

    MEAN_CIFAR10 = (0.4914, 0.4822, 0.4465)
    STD_CIFAR10 = (0.2023, 0.1994, 0.2010)

    tf_train = transforms.Compose(
        [
            transforms.ToPILImage(),
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(MEAN_CIFAR10, STD_CIFAR10),
        ]
    )
    if args.dataset == "CIFAR10":
        trainset = datasets.CIFAR10(root="data/CIFAR10", train=True, download=True)
    else:
        raise Exception("Invalid dataset")

    train_data_bad = DatasetBD(
        args,
        full_dataset=trainset,
        inject_portion=args.inject_portion,
        transform=tf_train,
        mode="train",
    )
    train_bad_loader = DataLoader(
        dataset=train_data_bad,
        batch_size=args.batch_size,
        shuffle=False,
    )

    return train_data_bad, train_bad_loader
