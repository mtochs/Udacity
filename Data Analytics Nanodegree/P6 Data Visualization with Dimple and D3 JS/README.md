#Data Visualization of Titanic Survival Rates with Dimple and D3 JS
**_Completed by Michael Ochs for Udacity Data Analytics Nanodegree_**

##Summary
The data visualization in this project illustrates the survival rate of passengers of the Titanic.  The survival rates are separated by class then gender.  The purpose of the visualization is to give a brief yet deeper look into who had the greatest and least chance of survival.  Upon inspection, it's clear that females in first class had the highest chance of survival and men in third class had the least chance of survival.

##Observation
The title "Surviving the Titanic: Rich Had Greatest Chance" emphasises that the rich--or first class passengers--had the greatest percentage chance of surviving the Titanic disaster.  The survival percentages decrease with the class.  Third class passengers had the lowest survival percentages for males and females.

##Design
The purpose of this visualization was to provide a quick reference for factors that correlated with Titanic passenger survival rates.  An analysis of the data was done previously where many factors were analyzed.  The correlation of survival rate with factors such as age, departure port, etc. were investigated.  The variables with the greatest correlation to survival rate were gender and passenger class.  Thus, this visualization encompasses those key variables for the viewer.

The design of this data visualization was modeled after an image generated in iPython notebook using the Titanic data.  The visual shows the survival rates of male and female passengers split by passenger class.  Figure 1 shows the mode generated from the ipython notebook drawing of Titanic survival percentages.  This was used as the first sketch for a visual.

![alt tag](https://github.com/mtochs/Udacity/blob/master/Data%20Analytics%20Nanodegree/P6%20Data%20Visualization%20with%20Dimple%20and%20D3%20JS/py_chart.png "Original chart from ipython notebook")
#####Figure 1: Original chart rendered in ipython notebook


Figure 2 shows the first attempt at a data visualization chart.

![alt tag](https://github.com/mtochs/Udacity/blob/master/Data%20Analytics%20Nanodegree/P6%20Data%20Visualization%20with%20Dimple%20and%20D3%20JS/d3_graph_v1.png "Initial Version of Titanic Data Visualization")
#####Figure 2: Initial version of Titanic Data visualization


Figure 3 is the final layout that was used for the data visualization project.  This visual was the final template used for the project.

![alt tag](https://github.com/mtochs/Udacity/blob/master/Data%20Analytics%20Nanodegree/P6%20Data%20Visualization%20with%20Dimple%20and%20D3%20JS/d3_graph_v2.png "Final Version of Titanic Data Visualization")
#####Figure 3: Final version of Titanic data visualization

##Feedback
This section includes all the feedback obtained from 3 individuals: persons A, B, and C.  Their feedback is included in parenthesis next to the subject in bold.

- **Colors** (A): One feedback mentioned that the colors are confusing and counterintuitive.  It's more commonly seen that male color is blue and female color is pink.  The pink might be too much of a contrast.  By default, male color was red and female color was blue.  Thus, the colors of red and blue were switched. 

- **Opacity** (B, C): Version 2 of the graph had an opacity setting of 1.  This correlates to no transparency.  Observes did not like it.  The complaint was that it made it harder to see where the bar chart fits against the axis.  Opacity was later adjusted to .7 (or 70%).

- **Age** (B): A suggestion was to split the data by age.  This suggestion was declined since it would add more clutter to the visualization.  As a result, it might take away from the emphasis that class had on survival.  Furthermore, there was a relatively small number of children in the data. Of the total 891 data points, 177 did not have age and 133 were less than 18 (i.e. 17 or younger).  In other words, only 12.7% of the data was of children. 

- **Data Order** (A, B, C): The first version did not have the classes in numerical order.  Class should be shown sequentially as 1, 2, 3.  In version 1 it was displayed as 1, 3, 2.  This critique was used to update the visualization to provide a clearer understanding on how passenger class correlated to survival rate.

- **Axis Titles** (A, B, C): The first versions did not have any titles.  It was suggested that the x and y axis are renamed to more intuitive names.  It was also recommended to create a title for the overall visualization.

##Resources
Initial data visualization framework provided by:
http://dimplejs.org/examples_viewer.html?id=bars_vertical_grouped

Final data visualization framework:
http://dimplejs.org/advanced_examples_viewer.html?id=advanced_bar_labels

Huge thank you to Myles Callan!!  Myles timeliness and thorough responses on the Udacity forum have been a huge help and guide in completing this project.
https://discussions.udacity.com/t/final-project-start/203226