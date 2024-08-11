# 🔹🔷Datatonic Challenge🔷🔹
Thank you for inviting me to complete this Challenge! 

Below is an overview of all the parts of the challenge, and my thinking associated with them.
I will also give an overview of the insights I collected in Part 3.

## Part 1 - Lord of the Rings 💍🌋
I approached this part by including books which had `"lord of the rings"` in the title, rather than explicitly being called `"lord of the rings"`.

**Some of the data considerations addressed during pre-processing:**
- Excluding books which had similar titles like "lords of the ring"
- Including only the earliest date of publication on books to reduce clutter in the date column of the CSV
- Only including works which had formats associated with books, due to a large amount of video games, movies, and CDs being included in the API response
    - ex. *Paperback, Hardcover, Binding, etc.*
- Excluding books which did not have an author listed, which mostly removed duplicates of books found in the API response

**Data about the books added to the CSV:**
- Title
- Author(s)
- Publish Year
- Publisher(s)
- Language

## Part 2 - Artificial Intelligence (AI) 🤖🧠
Here I made use of the [Subjects API](https://openlibrary.org/dev/docs/api/subjects) to create a dataset of works which tagged `"artificial intelligence"` as one of their associated subjects.

**Data about the books added to the CSV:**
- Title
- Author(s)
- Publish Year
- Subjects

## Part 3 - Insights 🧮📊
Using the CSV created in the previous step, I wanted to get insights on the growth and popularity of subjects associated with AI. 

I split up the data into 15 groups, and assigned subject keywords associated with the groups. 

**These groups were:**
1. Business and Economics
2. Computer Vision and Image Processing
3. Data Collection and Mining
4. Data Processing and Analysis
5. Databases and Management
6. Education and Learning
7. Healthcare and Medicine
8. Human-Computer Interaction and User Experience
9. Information Systems and Technology
10. Natural Langauge Processing and Lingustics
11. Neural Networks and Evolutionary Computation
12. Philosophy amd Ethics
13. Robotics and Automation
14. Science Fiction and Literature
15. Security and Privacy

**Some of the data considerations addressed while generating insights:**
- Excluding works published before 1950 to remove works with incorrect publish dates
  - *The earliest verifiable work associated with AI available on OpenLibrary is I, Robot by Isaac Asimov published in 1950*
  - ex. *Neural network research papers incorrectly stating they were published in 1899*
- Not considering works published after 2012 because this data skews the analysis of AI subject growth
  - *The number of works available on OpenLibrary across all subjects and fields drops drastically after 2011/2012, resulting in unreliable trends*
    
    ![Figure 1: Distribution of Categories in Works related to AI (1950-2024)](part3/charts/count_area_chart/count_area_chart_1950_2024.png)

    *Figure 1: Number of works published in each group by year (1950-2024)*
- Omitting the use of an "Other" group in the grouping of data to better showcase trends in selected groups

### Insights

