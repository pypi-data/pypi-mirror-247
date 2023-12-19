# ypkgupgr
## The pip package updater by yesseruser

This is a package updater that updates all outdated packages when run.  

This package works with Python 3.9+.

To install, follow the steps listed here:  
[Installation](https://github.com/yesseruser/ypkgupgr/wiki/Installation)

Here's the wiki page:  
[Wiki](https://github.com/yesseruser/ypkgupgr/wiki)

If you're running the package from a python file, please **use a subprocess** instead of importing and calling the `update_packages` function. This is because the package can update itself and can result in an error because of the code changing.
## What's Changed
* Added ignoring and unignoring packages by @yesseruser in https://github.com/Yesser-Studios/ypkgupgr/pull/6
* Moved log location by @yesseruser in https://github.com/Yesser-Studios/ypkgupgr/pull/6


**Full Changelog**: https://github.com/Yesser-Studios/ypkgupgr/compare/1.8.3...1.9.0
