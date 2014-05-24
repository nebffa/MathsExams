Maths Exams
===========


Maths Exams is an application for creating practice maths exams.


Why?
----

As a maths tutor I see students from public schools without enough practice exams to practice with in the leadup to their exam time. In my opinion, those schools don't have enough resources to provide them with the practice material they need.


What if?
--------

... we could generate educational content to serve that need using programming? This project explores that idea.


Installation
------------

```bash
1. Clone the repo
2. $ pip install -r requirements.txt
3. Ensure you have a LaTeX compiler so you can compile the generated LaTeX.
```


Run
---

Using Python 3:

```python
python exam.py
```

This creates `exam.tex`, a (very simple) exam in the same directory. It showcases all of the questions that have been created so far. Use your LaTeX compiler to create a `.pdf` and have a look!


Miscellaneous Information
-------------------------

These questions are based off the Victorian Certificate of Education (VCE) exams sat by year 12 students. Past papers
can be found at the [Victorian Curriculum Assessment Authority (VCAA) website](http://www.vcaa.vic.edu.au/Pages/vce/studies/mathematics/cas/casexams.aspx).


Contribute
----------


I don't know if there will be any demand for me to develop this further, so contributions of feedback instead of code are greatly appreciated!
