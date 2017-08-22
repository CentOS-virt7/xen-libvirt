# Introduction

This setup is meant to essentially track the Fedora packages.  There
is a branch called `fedora`, that will always mirror some version of a
Fedora repo.  Then there are Xen version branches: `xen-44`, `xen-46`,
and `xen-48`, which are for builds against Xen 4.4, 4.6, and 4.8
respectively.

It would be nice if we could simply pull directly from Fedora's git
repo; but for some reason the layout of the files within the repo is
different.  So instead, Fedora source rpms are occasionally downloaded
and "unpacked" into the repo to get updates.

# To update the Fedora branch

Check out the `fedora` branch:

    git checkout fedora

Download the newest version of the source rpm:

    wget http//${PATH}/libvirt-2.2.0-1.fc25.src.rpm

And "install" the RPM into the current directory:

    rpm --define "%_topdir `pwd`" -iv libvirt-2.2.0-1.fc25.src.rpm

This will overwrite SPECS/libvirt.spec with the new version.  Now commit those changes:

    git commit -a -m "Pull in 2.2.0-1.fc25"

# To pull those changes into a new branch

Check out the target branch:

    git checkout xen-46

Merge from the `fedora` branch:

    git merge fedora

This will almost certainly cause some conflicts in SPECS/libvirt.spec.
Go through the file looking for merge conflicts (demarcated with
`<<<<<<<<<`, `=========`, and `>>>>>>>>>`), and fix things up.

To begin with, simply try to fix up the merge conflicts reasonably,
then make a 'merge' commit:

    git add SPECS/libvirt.spec
    git commit -m "Merge"

Then try to build the RPM and fix up anything that's broken:

    rpmbuild --define "_topdir $PWD" -bb SPECS/xen.spec 

Finally add any future commits and send a pull request:

    git commit -a -m "Updates to 2.2.0-1"