### Install

To install the latest version of gazpacho run:

```
pip install -U gazpacho
```

### Changelog

#### 1.1.1-beta (Unreleased)

- Fix: headers issue (user agent) /u/lazerwarrior
- Fix: format() with void tags **@mickm3n**

#### 1.1 (2020-10-09)

- Feature: now [PEP 561](https://www.python.org/dev/peps/pep-0561/) compliant
- Feature: `Soup` now automatically formats and indents (pretty print) HTML where possible

#### 1.0 (2020-09-24)

- Feature: gazpacho is now fully baked with type hints (thanks for the suggestion [**@ju-sh**](https://github.com/ju-sh)!)
- Feature: `Soup.get("url")` alternative initializer
- Fixed: `.find` is now able to capture malformed void tags (`<img />`, vs. `<img>`) (thanks for the Issue [**@mallegrini**](https://github.com/mallegrini)!)
- Renamed: `.find(..., strict=)` is now `find(..., partial=)`
- Renamed: `.remove_tags` is now `.strip`


#### 0.9.4 (2020-07-07)

- Feature: automagical json-to-dictionary return behaviour for `get`
- Improvement: automatic missing URL protocol inference for `get`
- Improvement: condensed HTTPError Exceptions

#### 0.9.3 (2020-04-29)

- Updated the README (thanks for flagging the `lxml` error, [**@koaning**](https://github.com/koaning)!)

#### 0.9.2 (2020-04-21)

- Fixed `find(..., mode='first')` to return `None` and not an `IndexError` (thanks, [**@psyonara**](https://github.com/maxhumber/gazpacho/issues/14)!)

#### 0.9.1 (2020-02-16)

- Fixed `UnicodeEncodeError` lurking beneath `get` (thanks for the "Issue" [**@mlehotay**](https://github.com/mlehotay)!)
- Fixed `find` method to properly handle non-closing HTML tags

#### 0.9 (2019-11-25)

- Added the `remove_tags` method for isolating formatted text in a block of HTML

#### 0.8.1 (2019-10-10)

- Fixed empty element tag counting within the `find` method

#### 0.8 (2019-10-07)

* Added mode argument to the `find` method to adjust return behaviour (defaults to `mode='auto'`)
* Enabled strict attribute matching for the `find` method (defaults to `strict=False`)
