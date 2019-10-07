#### Contributing

When contributing to `gazpacho`, please open an issue before making a change



#### Development environment and steps

1. Install `pytest` either globally or in a virtualenv: `pip install pytest`
2. Click on the "Fork" button at the top-right of the GitHub page
3. Clone your fork: `git clone git@github.com:yourname/gazpacho.git`
4. Create a new branch to work on the issue/feature you want
5. Hack out your code. 
6. Runs the tests by executing `pytest` from the command line (tests live in the `tests` subfolder)
7. Submit a new PR with your code, indicating in the PR which issue/feature it relates to



#### Guidelines

- Keep in mind that `gazpacho` does not want to do everything. It is a replacement for BeautifulSoup and requests for **most** projects but **not all** projects
- Always write tests for any change introduced
- If the change involves new methods, arguments or otherwise modifies the public API, make sure to adjust the `README.md`
- If the change is beyond cosmetic, add it to the `CHANGELOG.md` file and give yourself credit!
