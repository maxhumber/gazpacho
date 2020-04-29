### Install

To install the latest version of gazpacho run:

```
pip install -U gazpacho
```



### Changelog

---

#### 0.9.3 (2020-04-29)

- Updated the README (thanks for flagging the `lxml` error, [@koaning](https://github.com/koaning)!)

#### 0.9.2 (2020-04-21)

- Fixed `find(..., mode='first')` to return `None` and not an `IndexError` (thanks, [psyonara](https://github.com/maxhumber/gazpacho/issues/14)!)

#### 0.9.1 (2020-02-16)

- Fixed `UnicodeEncodeError` lurking beneath `get` (thanks for the "Issue" [mlehotay](https://github.com/mlehotay)!)
- Fixed `find` method to properly handle non-closing HTML tags

#### 0.9 (2019-11-25)

- Added the `remove_tags` method for isolating formatted text in a block of HTML

#### 0.8.1 (2019-10-10)

- Fixed empty element tag counting within the `find` method

#### 0.8 (2019-10-07)

* Added mode argument to the `find` method to adjust return behaviour (defaults to `mode='auto'`)
* Enabled strict attribute matching for the `find` method (defaults to `strict=False`)
