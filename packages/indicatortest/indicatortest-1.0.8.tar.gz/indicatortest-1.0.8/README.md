Comments to appear in About dialog and first line on PyPI

Requirements
------------
**Ubuntu 20.04 or equivalent:** Using `GNOME Tweaks`, enable the `Ubuntu appIndicators` extension.

**Debian 11 / 12:** Install the `GNOME Shell` [extension](https://extensions.gnome.org/extension/615/appindicator-support/) 
`AppIndicator and KStatusNotifierItem Support`

Installation
------------
**Ubuntu / Debian:** Open a `terminal` and...
1. Install operating system packages:
```
sudo apt-get -y install gir1.2-ayatanaappindicator3-0.1 libcairo2-dev libgirepository1.0-dev pkg-config python3-dev python3-venv python3-notify2
```
2. Create a `Python` virtual environment, activate and install the indicator package:
```
python3 -m venv $HOME/.local/venv_indicatortest && \
. $HOME/.local/venv_indicatortest/bin/activate && \
python3 -m pip install indicatortest && \
deactivate
```
3. Copy icon, run script and desktop file to `$HOME/.local`:
```
mkdir -p $HOME/.local/share/icons/hicolor/scalable/apps && \
cp $HOME/.local/venv_indicatortest/lib/python3.*/site-packages/indicatortest/icons/hicolor/indicatortest.svg $HOME/.local/share/icons/hicolor/scalable/apps && \
mkdir -p $HOME/.local/bin && \
cp $HOME/.local/venv_indicatortest/lib/python3.*/site-packages/indicatortest/packaging/linux/indicatortest.sh $HOME/.local/bin && \
cp $HOME/.local/venv_indicatortest/lib/python3.*/site-packages/indicatortest/packaging/linux/indicatortest.py.desktop $HOME/.local/share/applications
```

Usage
-----
To run `indicatortest`, press the `Super`/`Windows` key to open the `Show Applications` overlay, type `test` into the search bar and the icon should be present for you to click.  If the icon does not appear, or appears as generic, you may have to log out and log back in (or restart).

Under the `Preferences` there is an `autostart` option to run `indicatortest` on start up.

Limitations
-----------
Distributions/versions with full functionality:
- `Debian 11 / 12`
- `Ubuntu 20.04 / 22.04`
- `Ubuntu Budgie 22.04`
- `Ubuntu Unity 20.04 / 22.04`

Distributions/versions with limited functionality:
- `Kubuntu 20.04 / 22.04` No mouse wheel scroll; tooltip in lieu of label.
- `Lubuntu 20.04 / 22.04` No label; tooltip is not dynamic; icon is not dynamic.
- `Ubuntu Budgie 20.04` No mouse middle click.
- `Ubuntu MATE 20.04` Dynamic icon is truncated, but fine whilst being clicked.
- `Ubuntu MATE 22.04` Default icon with colour change does not show up; dynamic icon for NEW MOON does not display.
- `Xubuntu 20.04 / 22.04` No mouse wheel scroll; tooltip in lieu of label.

Removal
-------
**Ubuntu / Debian:** Open a `terminal` and...
1. Remove operating system packages:
```
sudo apt-get -y remove gir1.2-ayatanaappindicator3-0.1 libcairo2-dev libgirepository1.0-dev pkg-config python3-dev python3-venv python3-notify2
```
2. Remove `Python` virtual environment and files from `$HOME/.local`:
```
rm -r $HOME/.local/venv_indicatortest && \
rm $HOME/.local/share/icons/hicolor/scalable/apps/indicatortest.svg && \
rm $HOME/.local/bin/indicatortest.sh && \
rm $HOME/.local/share/applications/indicatortest.py.desktop
```

License
-------
This project in its entirety is licensed under the terms of the GNU General Public License v3.0 license.

Copyright 2016-2023 Bernard Giannetti.

https://pypi.org/project/indicatortest
