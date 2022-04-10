# CARE ABOUT M.E. 

**Description**:  Menstrual Equity and Basic Needs Pantry inventory application for use by higher education institutions.

  - **Technology stack**: Django
  - **Status**:  Not maintained. 
  - **Platform Proposal Documents**: [Google Docs](https://drive.google.com/drive/folders/1JmWr6jCjmkuTKWWYdKnzseHvxjTa0v-e?usp=sharing). 
  - **Video**: [YouTube](https://youtu.be/Q2b08zN9JE4)

## Dependencies

Dependencies are installed during [installation](#installation). 

## Installation

```
git clone https://github.com/JDGi-Code/CARE-ABOUT-ME-App.git
cd ./CARE-ABOUT-ME-App/
pip install django
pip install sqlite
```

## Configuration

Change views in app/templates folder to customize layout.

## Usage

```
python manage.py runserver 8000
```
Users log in to submit tickets. 
Admin page exists at localhost:8000/admin.

## How to test the software

```
pip install seleniumbase
pip install pytest-django
```
Next run pytest on one of the test files (ie, in repositories folder).

## Known issues

There are currently no enabled reports capabilities. Reports can be generated from the database directly.

## Getting help

This application is not maintained. Please feel free to create an issue, and maybe someone from the community will support.

## Getting involved

Fork this repo, look through the issues, there is no active developer community at this moment.

----

## Open source licensing info
1. [GPLv3 LICENSE](LICENSE)

----

## Credits and references

1. [World Toilet Organization](https://www.worldtoilet.org/)
2. [UMass Undergraduate Research Project Presentation: CARE ABOUT M.E.](https://youtu.be/Q2b08zN9JE4)
3. [Crawford, Bridget, et al. “The Ground on Which We All Stand: A Conversation About Menstrual Equity Law and Activism.” Michigan Journal of Gender & Law, vol. 26, no. 2, Mar. 2020, pp. 341–88](https://doi.org/10.36641/mjgl.26.2.ground) 
