# 🔹🔷Datatonic Challenge🔷🔹
Thank you for inviting me to complete this Challenge! 

Below is an overview of all the parts of the challenge, and my thinking associated with them.
I will also give an overview of the insights I collected in Part 3.

## Part 1 - Lord of the Rings
The way I approached this part was by including books which had `"lord of the rings"` in the title, rather than explicitly being called `"lord of the rings"`.

**Some of the data considerations addressed during pre-processing:**
- Excluding books which had similar titles like "lords of the ring"
- Including only the earliest date of publication on books to reduce clutter in the date column of the CSV
- Only including works which had formats associated with books due to a large amount of video games, movies, and CDs being included in the API response
    - ex. Paperback, Hardcover, Binding, etc.
- Excluding books which did not have an author listed, which mostly removed duplicates of books found in the API response

**Data about the books added to the CSV:**
- Title
- Author(s)
- Publish Year
- Publisher(s)
- Language

## Part 2 - Artificial Intelligence
Here I made use of the [Subjects API](https://openlibrary.org/dev/docs/api/subjects) to create a dataset of works which tagged `"artificial intelligence"` as one of the associated subjects.

**Data about the books added to the CSV:**
- Title
- Author(s)
- Publish Year
- Subjects

## Part 3 - Insights
