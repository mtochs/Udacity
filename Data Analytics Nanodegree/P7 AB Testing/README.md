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

- **Retention (d<sub>min</sub>=0.01):** This is the number of user-ids to remain enrolled past the 14-day boundary--and thus make at least one payment--divided by number of user-ids to complete checkout.  This metric is also affected by the free trial screener question.  If the hypothesis is correct, we should see a difference in retention of the control and experiement groups.

- **Net conversion (d<sub>min</sub>=0.0075):** This number is the user-ids to remain enrolled past the 14-day boundary--and thus make at least one payment--divided by the number of unique cookies to click the "Start free trial" button.  If the free trial screener has an affect on retention, then this should also vary.

###Unused Metric
- **Number of user-ids d<sub>min</sub>=50):** That is, number of users who enroll in the free trial.  This is not a suitable invariant metric since a user must enroll in order to be tallied.  It also would not necessarily change due to the free trial screener for many reasons.  For example, there can be many user-ids per person.

##Measuring Standard Deviation
Analytics estimates for standard deviation given a sample size of 5000 page-view cookies as follows:
- **Gross Conversion:** 0.202
- **Retention:** 0.0549
- **Net conversion:** 0.0156




##Resources
Udacity A/B Test Final Project Instructions provided by:
https://docs.google.com/document/u/0/d/1aCquhIqsUApgsxQ8-SQBAigFDcfWVVohLEXcV6jWbdI/pub?embedded=True

