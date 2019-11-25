### Install

To install the latest version of gazpacho run:

```
pip install -U gazpacho
```



### Changelog

---

#### 0.9 (2019-11-25)

- Added the `remove_tags` method for isolating formatted text in a block of HTML

#### 0.8.1 (2019-10-10)

- Fixed empty element tag counting within the `find` method

#### 0.8 (2019-10-07)

* Added mode argument to the `find` method to adjust return behaviour (defaults to `mode='auto'`)
* Enabled strict attribute matching for the `find` method (defaults to `strict=False`)
