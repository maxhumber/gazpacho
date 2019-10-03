#### Contributing

When contributing to `gazpacho`, please open an issue before making a change.



#### Development environment and steps

1. Install `pytest` either globally or in a virtualenv: `pip install pytest`.
2. Click on the "Fork" button at the top-right of the GitHub page.
3. Clone your fork. Example: `git clone git@github.com:yourname/gazpacho.git`.
4. Create a new branch to work on the issue/feature you want.
5. Hack out your code. To run the tests, just run `pytest`. Tests live in the `tests`subfolder.
6. Submit a new PR with your code, indicating in the PR which issue/feature it relates to.



#### Guidelines

- Remember that `gazpacho` does not want to do everything. Its scope is to serve as a replacement for BeautifulSoup and requests for **most** projects but not all projects. If the feature you want to implement adds a lot of complexity to the code, think twice if it is really needed or can be worked around in a few lines.
- Always write tests for any change introduced.
- If the change involves new options or modifies the public interface, modify also the `README` file explaining how to use it.
- If the change is not just cosmetic, add a line to the CHANGELOG.md file



### 