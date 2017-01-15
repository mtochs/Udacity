#A/B Testing
**_Completed by Michael Ochs for Udacity Data Analytics Nanodegree_**

##Experiment Overview: Free Trial Screener
At the time of this experiment, Udacity courses currently have two options on the home page: "start free trial", and "access course materials". If the student clicks "start free trial", they will be asked to enter their credit card information, and then they will be enrolled in a free trial for the paid version of the course. After 14 days, they will automatically be charged unless they cancel first. If the student clicks "access course materials", they will be able to view the videos and take the quizzes for free, but they will not receive coaching support or a verified certificate, and they will not submit their final project for feedback.

In the experiment, Udacity tested a change where if the student clicked "start free trial", they were asked how much time they had available to devote to the course. If the student indicated 5 or more hours per week, they would be taken through the checkout process as usual. If they indicated fewer than 5 hours per week, a message would appear indicating that Udacity courses usually require a greater time commitment for successful completion, and suggesting that the student might like to access the course materials for free. At this point, the student would have the option to continue enrolling in the free trial, or access the course materials for free instead. This screenshot shows what the experiment looks like.

The hypothesis was that this might set clearer expectations for students upfront, thus reducing the number of frustrated students who left the free trial because they didn't have enough time—without significantly reducing the number of students to continue past the free trial and eventually complete the course. If this hypothesis held true, Udacity could improve the overall student experience and improve coaches' capacity to support students who are likely to complete the course.

The unit of diversion is a cookie, although if the student enrolls in the free trial, they are tracked by user-id from that point forward. The same user-id cannot enroll in the free trial twice. For users that do not enroll, their user-id is not tracked in the experiment, even if they were signed in when they visited the course overview page.

##Metric Choice

###Choosing Invariant Metrics
- **Number of cookies (d<sub>min</sub>=3000):** This is the number of unique cookies to view the course overview page.  Thus, it should not vary between control and experiment groups.  The number is tallied before the user clicks anything beyond the course overview.

- **Number of clicks (d<sub>min</sub>=240):** This is the number of unique cookies to click the "Start free trial" button which happens before the free trial screener is triggered.  This metric should also be evenly distributed amongst the control and groups since the free trial screener has not yet triggered.

- **Click-through-probability (d<sub>min</sub>=0.01):**  Defined as the number of unique cookies to click the "Start free trial" button divided by number of unique cookies to view the course overview page.  This is essentially a division of the above metrics.  Thus, this should not be affected if the above metrics are not affected.

###Choosing Evaluation Metrics
- **Gross Conversion (d<sub>min</sub>=0.01):** Illustrates the number of user-ids to complete checkout and enroll in the free trial divided by number of unique cookies to click the "Start free trial" button.  This is a good choice for an evaluation metric since it's directly affected by clicking on "start free trial".  Thus, the number is affected by the free trial screener question.

- **Net conversion (d<sub>min</sub>=0.0075):** This number is the user-ids to remain enrolled past the 14-day boundary--and thus make at least one payment--divided by the number of unique cookies to click the "Start free trial" button.  If the hypothesis is correct, we should see a difference in retention of the control and experiement groups.

###Unused Metric
- **Number of user-ids d<sub>min</sub>=50):** That is, number of users who enroll in the free trial.  This is not a suitable invariant metric since a user must enroll in order to be tallied.  It also would not necessarily change due to the free trial screener for many reasons.  For example, there can be many user-ids per person.

- **Retention (d<sub>min</sub>=0.01):** This is the number of user-ids to remain enrolled past the 14-day boundary--and thus make at least one payment--divided by number of user-ids to complete checkout.  This metric is also affected by the free trial screener question.  This metric is not used since it is proportional to Net Conversion and Gross Conversion; however, it is not a factor of the unit of diversion.

##Measuring Standard Deviation
Analytics estimates for standard deviation given a sample size of 5000 page-view cookies as follows:
- **Gross Conversion:** 0.202
- **Net conversion:** 0.0156

Gross Conversion and Net Conversion are both a factor of the number of cookies (i.e. the unit of diversion).  Thus, analytical estimates of variance can be used.

##Sizing

Project baseline values:
- Unique cookies to view page per day: 40000
- Unique cookies to click "Start free trial" per day: 3200
- Enrollments per day: 660
- Click-through-probability on "Start free trial": 0.08
- Probability of enrolling, given click: 0.20625
- Probability of payment, given enroll: 0.53
- Probability of payment, given click: 0.1093125

#####Note: Bonferroni correction not used

###Choosing Number of Samples Given Power
Total pageviews needed to collect to adequately power the experiment using alpha=0.05 and beta=0.2:
- **Gross Conversion:** 645,875
- **Net conversion:** 685,325

Based on this we need a total pageview of 685,325.

###Duration vs. Exposure
Using 40,000 for unique cookies per day we would need the following days for each percentage of diversion:
- 100% diverted would need 18 days
- 80% diverted would need 22 days
- 50% diverted would need 35 days

#####Note: all "day" values are rounded up.

A diverted percentage of 80% was used for this experiment.  The experiment does not appear to be a huge factor to user satisfaction.  Thus, we feel confident that diverting a higher number should not pose any significant impacts to Udacity.  Nevertheless, there could be issues with coding, etc.  So, we would not want to divert 100% in the event of a web coding bug that might reduce customer experience.

Diverting 80% seems reasonable since the data could be collected inside of a month.  That would allow this experiment to be executed multiple times in a year if seasonality might be a factor for future experiments.

##Experiment Analysis
###Sanity Checks
Below are the values expected to be observed, the actual observed value, and whether the metric passes a sanity check using a 95% confidence interval (CI).

| Metric | Expected | Observed | CI Lower | CI Upper | Pass? |
| ------ | -------- | -------- | -------- | -------- | ----- |
| Number of Cookies | 0.5000 | 0.5006 | 0.4988 | 0.5012 | Yes |
| Number of Clicks | 0.5000 | 0.5005 | 0.4959 | 0.5042 | Yes |
| Click-through-probability | 0.0821 | 0.0822 | 0.0812 | 0.0830 | Yes |

###Result Analysis
####Effect Size Tests
Below are the differences between the experiment and control groups for the evaluation metrics.  A 95% confidence interval (CI) is used.  It is indicated whether each metric is statistically (SS) and practically (PS) significant.

| Metric | Difference | CI Lower | CI Upper | SS | PS |
| ------ | ---------- | -------- | -------- | --- | --- |
| Gross Conversion | -0.0205 | -.0291 | -.0120 | X | X |
| Net Conversion | -0.0048 | -0.0116 | 0.0019 |   |   |

####Sign Tests
Below are the values from a sign test using the day-by-day data. The p-value of the sign test are included.  It is indicated if the evaluation metrics is statistically significant (SS).

| Metric | P-Value | SS |
| ------ | ------- | --- |
| Gross Conversion | 0.0026 | X |
| Net Conversion | 0.6776 |   |

####Summary
A project was conducted with the focus on determining how setting clearer expectations might affect the number of frustrated students.  The hope is that this would boost student experience and improve coaches' capacity to support students.  This in turn would increase the number of students that completed the course.

Three invariant metrics were used in the project: number of cookies, number of clicks, and click-through-probability.  The evaluation metrics used were gross conversion and net conversion.  In order for the hypothesis to be true--and the null to be rejected--all invariant metrics must have remained within a 95% confidence interval while simultaneously showing improvement in one or both evaluation metrics.

All invariant metrics remained within a 95% confidence interval and gross conversion was shown to have a statistically and practially significant difference.  Net conversion did not show a statistically or practially significant difference.

Bonferroni correction was not used for this project.  The Bonferroni correction is used for concerns on false positives.  If multiple comparisons are done or multiple hypotheses are tested, the chance of a rare event increases, and therefore, the likelihood of incorrectly rejecting a null hypothesis (i.e., making a Type I error) increases.[4]  Thus Bonferroni compensates for an increase in false positives.  This project does not utilize many invariant or evaluation metrics nor does have have multiple hypothesis.  It is for this reason that it was not incoporated into this project.

###Recommendation
The null hypotheses is rejected since all invariant metrics remained in a 95% confidence interval while the gross conversion difference between the control and observed groups were shown to be statistically and practially significant.  It is for this reason we would suggest implementing this change.

Furthermore the changes tested in this experiement were not highly invasive.  The changes should not create a significant--or perhaps even noticeable--change in student experience.  To say it another way: the gains outweigh the risks.

##Follow-Up Experiment
A follow up experiement to further increase customer experience could be to have a coach message someone who has signed up but is not utilizing the web site.  The criteria would be people that signed up with a site utilization of less than 5 hours by the 7th day.  A dialogue window could pop up on the site to ask something simple like "how is the training going?  Do you need any help?"  The unit of diversion could be user-id to follow the users that fit the criteria of the project.  All users that signed up for the course would need a user-id.

The hypotheses for this project is that intervention with users on the 7th day of the trial that have fallen below 5 hours of usage will increase student completion rates.  Students that are not using the site the recommended 5 hours per week may be more responsive to a simple line of communication from a coach.  At that point the student could respond with areas where they are struggling.  Thus, students would work to completion if those barriers are removed.

The invariant metrics would be:
- **Numbers of cookies:** The number of unique cookies that viewed the web site.  This number should not change if students receive a dialogue window inquiring about the course experience or not.
- **Number of clicks:** The number of clicks before a dialogue window appears inquiring about course experience.  This number should also remain the same provided there are no other significant changes are being made to the web site.

The evaluation metrics would be:
- **Net conversion:** This number is the user-ids to remain enrolled past the 14-day boundary--and thus make at least one payment--divided by the number of unique cookies to click the "Start free trial" button.  This number should improve if the hypothesis is true.  The number of users to enroll past 14 days should increase if the inquiry dialogue improves customer experience.






##Resources
[1] Udacity A/B Test Final Project Instructions: 
https://docs.google.com/document/u/0/d/1aCquhIqsUApgsxQ8-SQBAigFDcfWVVohLEXcV6jWbdI/pub?embedded=True

[2] Udacity A/B Test Baseline Values: 
https://docs.google.com/spreadsheets/d/1MYNUtC47Pg8hdoCjOXaHqF-thheGpUshrFA21BAJnNc/edit#gid=0

[3] Udacity A/B Test Data Set: 
https://docs.google.com/spreadsheets/d/1Mu5u9GrybDdska-ljPXyBjTpdZIUev_6i7t4LRDfXM8/edit#gid=0

[4] Wikipedia: Bonferroni correction 
https://en.wikipedia.org/wiki/Bonferroni_correction