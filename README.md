# Welcome to the Waterboard code base!



### Setup

    npm i
    npm run dev



Water Point Dashboard / Filter Page
---

- Map
   - has search place by name enabled
- Horizontal Bar Charts
  - "3 types"
    - with pagination (tabyia, funded) 
- Info chart (beneficiaries)
- Pie Chart
- Last Update Table

Water Point Table Report Page
---

- Download data as CSV
- Download data as SHP
- Data Table
  - Row on click open feature by uuid
  - Text Search
  - Pagination
  - Info
  - Numbers per Page



Water Point Feature Detail Page
---

### Update Water point

- line charts
  - has tooltip
- Data Table
  - Water point Row on click open modal with disabled form
  - Pagination
  - Info
  - Numbers per Page
- Map
  - zoom control
  - layer control with layers
  - single marker
    - on drag end updates form lat, lng
- Form
  - disabled by default, enabled on Enable Edit button click
  - accordion
  - on submit error returns form html string with error labels
  - on lat, lng update will update marker position and center map

### Add Water point

- Map
  - zoom control
  - layer control with layers
  - single marker
    - on drag end updates form lat, lng
- Form
  - enabled by default
  - accordion
  - on submit error returns form html string with error labels
  - on lat, lng update will update marker position and center map


Admin Pages:
---


Dashboard / Index Page
----

### Map


General
---


# License

Code: [MIT License](https://choosealicense.com/licenses/mit/)

Out intention is to foster wide spread usage of the data and the code that we
provide. Please use this code and data in the interests of humanity and not for
nefarious purposes.
