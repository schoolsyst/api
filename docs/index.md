# schoolsyst's API

## Authentification

All routes require a JWT token to access (except `/auth/` routes)

To access routes, first [obtain your token](#routes-auth), then, pass it in the `Authorization` header using the format `Bearer <your token>`.

## Routes

### POST /auth/

> Obtain a JWT token, given a email and a password.

Provide the `email` and `password` in the request's body as such:

```json
{
  "email": "<your email>",
  "password": "<your password>"
}
```

The response will be of the following form:

```json
{
  "access": "<your access token>",
  "refresh": "<your refresh token>"
}
```

### POST /auth/refresh/

> Renew your access token provided the refresh token

Given the refresh token:

```json
{
  "refresh": "<your refresh token>"
}
```

The response will contain the new access token:

```json
{
  "access": "<your new access token>",
}
```

### GET /users/self/

> Information about the current user (the one authentificated by the access token)

The response will contain:

- `email` - unique (case insensitive)
- `activated` - Whether or not the user has confirmed his email address.

### POST /users/

> Create an account.

The request must contain:

- email
- password

Upon registration, the API...

1. creates a new unique activation token and saves it on `<the user>.activation_token`
2. sends a confirmation email to `email`, this email contains a button that links to `https://api.schoolsyst.com/users/activate/?token=<the verify token>&email=<the email address>`

### POST /users/activate

Query parameters:

| Name  | Type          | Constraints            | Description                                                                                    |
| ----- | ------------- | ---------------------- | ---------------------------------------------------------------------------------------------- |
| email | email address | Exists in the database |
| token | string        | Exists in the database | Stored as a property named `activation_token` on each user. Destroyed 24 hours after creation. |

---

Routes beyond this point require the user to have its activation state (`activated` property) set to `true`. Otherwise a `401 Unauthorized` response will be sent.

From here, all resources are tied to a user, and all have creation and last updated date read-only fields, named respectively `created_at` and `updated_at`

---

### /settings/

Settings of the user.

| Name               | Type                             | Constraints       | Default value                                                          | Description                                                                                                                                                                                                                                      |
| ------------------ | -------------------------------- | ----------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| theme              | One of 'light', 'dark' or 'auto' | 'auto'            |
| year_layout        | daterange[]                      | array.length >= 1 | _required_                                                             | Configures how the year is split. For example, for a student whose school works on semesters, the layout will be `[{start: <start of the year>, end: <end of the first semester>}, {start: <start of the 2nd semester, end: <end of the year>}]` |
| starting_week_type | 'even' or 'odd'                  | 'even'            | Whether the first week of school is an 'odd'-type week of 'even'-type. |
| grades_unit        | float                            | > 0               | _required_                                                             | What unit is used to display grades. Note that grades are stored as floats in [0; 1], no matter what this value is set to.                                                                                                                       |
| offdays            | daterange[]                      |                   | `[]`                                                                   | Holidays, exceptional weeks without courses, school trips, etc.                                                                                                                                                                                  |

NOTE: This endpoint only accepts `GET` and `PATCH` requests, not `POST` (you cannot create _new_ settings)

### /subjects/

| Name   | Type              | Constraints                                    | Default value | Description                                                                                                                     |
| ------ | ----------------- | ---------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| name   | string            | max length: 100                                | _required_    | The subject's display name.                                                                                                     |
| slug   | slug              | max length: 100<br>must be unique to the user. | _required_    | Derived from the `name`, contains only alphanumerical characters and the dash "-". Case insensitive.                            |
| color  | int (hexadecimal) | must be a valid hex color value                | `0x000000`    |
| weight | float             | >= 0                                           | 1             |                                                                                                                                 |
| goal   | float             | ∈ [0; 1]                                       |               |
| room   | string            | max length: 100                                |               | If the courses of the subject are always in the same room, it's set here and will serve as a default for the "add event" modal. |

### /homework/

> Represents homework

The endpoint `GET /homework/` only returns homework that is not due in the past or not completed (`progress != 1`).
To include old & completed homework, do a request to `GET /homework?include-old`. The response to this endpoint will be paginated, at a rate of 200 items per page.

| Name         | Type                                                  | Constraints                              | Default value | Description                             |
| ------------ | ----------------------------------------------------- | ---------------------------------------- | ------------- | --------------------------------------- |
| title        | string                                                | max length: 500                          | _required_    |
| subject      | Subject object                                        |                                          | _required_    |
| type         | one of 'test', 'coursework', 'to_bring' or 'exercise' |                                          | _required_    |
| completed_at | datetime                                              | must be in the past (≤ now)<br>read-only | `null`        | The last time `progress` was set to `1` |
| progress     | float                                                 | ∈ [0; 1]                                 | 0             | 0 means not started, 1 means finished.  |
| notes        | Note[]                                                | notes must be owned by the user          | `[]`          | Linked notes                            |
| grades       | Grade[]                                               | grades must be owned by the user         | `[]`          | Linked grades.                          |

### /grades/

| Name        | Type     | Constraints         | Default value | Description                                                             |
| ----------- | -------- | ------------------- | ------------- | ----------------------------------------------------------------------- |
| title       | string   | max length: 500     | _required_    |
| actual      | float    | ∈ [0; 1]            | `null`        | The actual mark                                                         |
| expected    | float    | ∈ [0; 1]            | `null`        | The mark the user thought it would get after doing the test             |
| goal        | float    | ∈ [0; 1]            | `null`        | The goal mark                                                           |
| unit        | float    | > 0                 | _required_    |
| weight      | float    | >= 0                | 1             |
| obtained_at | datetime | must be in the past | `null`        | The datetime where `actual` was first set to a value other than `null`. |

### /notes/

| Name      | Type                                                | Constraints     | Default value                          | Description                                                                                                    |
| --------- | --------------------------------------------------- | --------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| name      | string                                              | max length: 500 | ""                                     |
| content   | string                                              |                 | ""                                     | `content` is omitted from the `GET /events/` but is present when requesting a single note (`GET /notes/:uuid`) |
| thumbnail | string                                              | read-only       | `/notes/<uuid of this note>/thumbnail` |
| type      | One of 'html', 'markdown', 'asciidoc' or 'external' |                 | 'html'                                 | For 'external' notes, the content is the URL pointing to the note.                                             |
| quizzes   | quiz[]                                              |                 | `[]`                                   | Linked quizzes.                                                                                                |

The response is paginated, at a rate of 100 items per page.

### GET /notes/:uuid/convert/:format

> Get the content of a note as a specific format. Typically used by the "export" modal on the frontend.

`:format` can be one of:

- pdf
- tex
- docx
- txt
- odt
- markdown
- asciidoc
- rst
- epub
- mediawiki

NOTE: Pandoc is used for converting notes, and the following mappings are made for formats:

| `:format` | Given to pandoc                               |
| --------- | --------------------------------------------- |
| markdown  | markdown_phpextra+emoji+superscript+subscript |
| tex       | latex                                         |
| txt       | plain                                         |

NOTE: Some formats output binary files. Their MIME types are set correctly by the response:

| `:format`     | Response's MIME Type                                                    |
| ------------- | ----------------------------------------------------------------------- |
| docx          | application/vnd.openxmlformats-officedocument.wordprocessingml.document |
| pdf           | application/pdf                                                         |
| odt           | application/vnd.oasis.opendocument.text                                 |
| _all  others_ | text/plain                                                              |

### POST /notes/convert/:in_format/:out_format

> Converts the request body (in `:in_format`) into `:out_format`.

Example:

```html
POST /notes/convert/html/pdf
Authorization: Bearer SOME_TOTALLY_ACCEPTABLE_ACCESS_TOKEN

<h1>Hello</h1>
```
 
Will convert some HTML text (`<h1>Hello</h1>`) into a PDF and return that file.
Typically used for importing notes.

Possible values of `:in_format` and `:out_format`: See `GET /notes/:uuid/convert/:format`'s `:format` possible values.

### /quizzes/

| Name        | Type          | Constraints         | Default value | Description                                                                            |
| ----------- | ------------- | ------------------- | ------------- | -------------------------------------------------------------------------------------- |
| name        | string        | max length: 500     | _required_    |
| questions   | Question[]    |                     | `[]`          | An array of questions. The definition of those object is still a work in progress.     |
| tries.test  | integer       | >= 0                | 0             | Number of trials in test mode                                                          |
| tries.train | integer       | >= 0                | 0             | Number of trials in train mode                                                         |
| tries.total | integer       | >= 0                | 0             | Total number of trials                                                                 |
| modified_at | datetime      | must be in the past | `now()`       | When was `questions` or `name` last modified                                           |
| time_spent  | integer       | >= 0                | 0             | (in seconds) the total time spent on this quizz                                        |
| sessions    | QuizSession[] |                     | `[]`          | An array of quiz sessions. The definition of those object is still a work in progress. |
| notes       | Note[]        |                     | `[]`          | Referenced notes.                                                                      |

---

CLARIFICATION: event(s) vs course(s)

- events are "base" events as returned by the /events/ API endpoint.
  They describe a normal week of the year
- courses are events, with deletions, additions and offdays applied.
  They have a `date` attribute and describe a *particular* week, and thus are tied to a date range, a specific week of the year.

---

### /events/

> Events of the schedule

| Name          | Type           | Constraints                               | Default value | Description                              |
| ------------- | -------------- | ----------------------------------------- | ------------- | ---------------------------------------- |
| subject       | Subject object |                                           | _required_    | The linked subject                       |
| start         | time           |                                           | _required_    |
| end           | time           | must be in the future relative to `start` | _required_    |
| day           | integer        | ∈ [1; 7]                                  | _required_    | 1 is monday, 7 is  sunday (ISO weekdays) |
| room          | string         | max length: 100                           | ""            |
| on_even_weeks | boolean        |                                           | `true`        | This event happens on even weeks         |
| on_odd_weeks  | boolean        |                                           | `true`        | This event happens on odd weeks          |

### /events/mutations/

> Mutations on the schedule

| Name       | Type         | Constraints               | Default value | Description |
| ---------- | ------------ | ------------------------- | ------------- | ----------- |
| event      | Event object | Must be owned by the user | `null`        |
| deleted_in | daterange    |                           | `null`        |
| added_in   | daterange    |                           | `null`        |
| room       | string       |                           | `null`        |

Multiple interpretations occur following which values are taken by `added_in` and `deleted_in`

 | &nbsp;     | added_in && deleted_in | added_in && !deleted_in | !added_in && deleted_in | !added_in && !deleted_in |
 | ---------- | ---------------------- | ----------------------- | ----------------------- | ------------------------ |
 | `subject`  | EDT                    | Ø                       | Ø                       | Ø                        |
 | !`subject` | RES                    | ADD                     | DEL                     | Ø                        |

| Type of mutation | meaning                                                                                | example                                                                                          |
| ---------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| EDT              | A simple editing of the course, while keeping it on the same day.                      | For the 2019-12-08 Physics course from 08:00 to 08:55, the room is L013 and not L453             |
| RES              | A rescheduling. The room and other info may also be changed for the rescheduled event. | The 2019-08-12 Mathematics course from 13:05 to 14:00 is moved to 2019-08-14 from 08:00 to 08:55 |
| ADD              | An exceptional course that is not part of the regular schedule.                        | An exceptional History course will be added at 2019-07-11, from 16:45 to 18:00                   |
| DEL              | A removal of course, without rescheduling.                                             | The 2020-01-13 Chemistry course from 15:50 to 16:45 is cancelled                                 |

### GET /courses/:start/:end

> Get courses within an interval (inclusive on both ends).

| Name    | Type           | Constraints                               | Description        |
| ------- | -------------- | ----------------------------------------- | ------------------ |
| subject | Subject object |                                           | The linked subject |
| start   | datetime       |                                           |                    |
| end     | datetime       | must be in the future relative to `start` |                    |
| room    | string         | max length: 100                           |                    |
