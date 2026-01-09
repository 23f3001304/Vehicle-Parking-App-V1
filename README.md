# Vehicle-Parking-App-V1
<table style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
  <tr>
    <td style="padding: 10px; font-weight: bold; text-align: left;">Nickname:</td>
    <td style="padding: 10px; background: #eee;">ParkEase</td>
  </tr>
  <tr>
    <td style="padding: 10px; font-weight: bold; text-align: left;">Created by:</td>
    <td style="padding: 10px; background: #eee;">Vishesh Daga</td>
  </tr>
  <tr>
    <td style="padding: 10px; font-weight: bold; text-align: left;">Company:</td>
    <td style="padding: 10px; background: #eee;">Drdo</td>
  </tr>
    <tr>
    <td style="padding: 10px; font-weight: bold; text-align: left;">FrontEnd:</td>
    <td style="padding: 10px; background: #eee;">Jinja Templates, Css, Js</td>
  </tr>
    <tr>
    <td style="padding: 10px; font-weight: bold; text-align: left;">Backend:</td>
    <td style="padding: 10px; background: #eee;">Flask, Sqlite, SqlAlchemy</td>
  </tr>
      <tr>
    <td style="padding: 10px; font-weight: bold; text-align: left;">Security:</td>
    <td style="padding: 10px; background: #eee;">Flask login , werkzeug</td>
  </tr>
</table>

## How to Start My flask app in localHost

### Prerequisites
- Python 3.7 or higher
- Git (for cloning the repository)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/23f3001304/Vehicle-Parking-App-V1.git
   cd Vehicle-Parking-App-V1
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables** (Optional)
   ```bash
   # Create a .env file for custom configuration
   echo "DEBUG=True" > .env
   echo "SECRET_KEY=your-secret-key-here" >> .env
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```
   *Note: The database will be automatically initialized on first run*

6. **Access the Application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`
   - You should see the ParkEase login page

### Default Admin Access
The application will create default admin credentials on first run. Check the database initialization in `db.py` for specific credentials.

### Stopping the Application
- Press `Ctrl+C` in the terminal to stop the server
- Deactivate the virtual environment: `deactivate`

## App Overview and Design Process
Since the project was about creating a WebApp around parking, I began by analyzing the provided wireframe and creating a rough design in Figma. As for the name I just thought to go simple and called it ParkEase

The rough figma design from which i started working on the app can be accessed from this link:
https://www.figma.com/design/bkk2cCdedvK0zNqE0nw64V/ParkEase?node-id=0-1&t=FzAzgsTsETof1KOO-1

Some of the Photos taken from current design are:

*Login Screen:*

<img width="2560" alt="Login Screen" height="1600" alt="image" src="https://github.com/user-attachments/assets/11feaac6-84f9-414f-a9d7-b3acb840bd54" />


*SignUp Screen:*

<img width="2559" height="1599" alt="Sign Up Screen" src="https://github.com/user-attachments/assets/4d4552f8-2bc1-4566-a0e0-6bc87db94656" />


*Admin Dashboard with Toast:*

<img width="2555" height="1599" alt="Admin Dashboard with Toast" src="https://github.com/user-attachments/assets/3fcb1675-8800-4d5b-b13b-56b644aa6c5b" />


*Spot Dashboard:*

<img width="2559" height="1599" alt="Spot Dashboard" src="https://github.com/user-attachments/assets/f62dd9dc-df73-4250-9a98-de0536fcb567" />


## Project Structure
Here is the Project Strcuture for the whole app :

```
Vehicle-Parking-App-V1/
├── 📁 controllers/                    # Business logic layer
│   ├── __init__.py
│   ├── auth_controller.py
│   ├── base_controller.py
│   ├── 📁 Admin/                      # Admin-specific business operations
│   │   ├── __init__.py
│   │   ├── admin_controller.py
│   │   ├── admin_utils.py
│   │   ├── lot.py
│   │   ├── spot.py
│   │   └── 📁 utils/                  # Admin utility functions
│   │       ├── getter.py
│   │       └── lot_utils.py
│   └── 📁 User/                       # User-specific business operations
│       ├── __init__.py
│       ├── reservation_controller.py
│       └── user_controller.py
├── 📁 models/                         # Data models - defines database structure and relationships
│   ├── __init__.py
│   ├── Admin.py
│   ├── Base.py
│   ├── ParkingLot.py
│   ├── ParkingSpot.py
│   ├── Reservation.py
│   └── User.py
├── 📁 routes/                         # URL routing - maps URLs to controller functions
│   ├── __init__.py
│   ├── admin_routes.py
│   ├── auth_routes.py
│   └── user_routes.py
├── 📁 static/                         # Frontend assets - CSS, JavaScript, images, icons
│   ├── 📁 css/                        # Stylesheets for UI components
│   │   ├── dashboard.css
│   │   ├── font.css
│   │   ├── parking_lot.css
│   │   ├── search.css
│   │   ├── sidebar.css
│   │   ├── summary.css
│   │   ├── summary_simple.css
│   │   ├── toast.css
│   │   ├── user.css
│   │   ├── user_summary.css
│   │   ├── users.css
│   │   └── 📁 forms/                  # Form-specific styling
│   │       ├── common.css
│   │       └── 📁 auth/               # Authentication form styles
│   │           ├── login.css
│   │           └── signup.css
│   ├── 📁 images/                     # Static images and graphics
│   │   ├── Log_sidebar.png
│   │   ├── Lot.png
│   │   └── spot.png
│   ├── 📁 js/                         # Client-side JavaScript functionality
│   │   ├── add_Lot.js
│   │   ├── dashboard.js
│   │   ├── edit_Lot.js
│   │   ├── login.js
│   │   ├── search.js
│   │   ├── sidebar.js
│   │   ├── signup.js
│   │   ├── summary.js
│   │   ├── summary_apexcharts.js
│   │   ├── summary_simple.js
│   │   ├── user_dashboard.js
│   │   └── user_summary.js
│   ├── 📁 svg/                        # Scalable vector graphics and icons
│   │   ├── Address.svg
│   │   ├── AdminAvatar.svg
│   │   ├── car.svg
│   │   ├── Chevron_Right.svg
│   │   ├── danger.svg
│   │   ├── Email.svg
│   │   ├── House_01.svg
│   │   ├── Icon.svg
│   │   ├── id.svg
│   │   ├── Map.svg
│   │   ├── Password.svg
│   │   ├── Pincode.svg
│   │   ├── price.svg
│   │   ├── spots.svg
│   │   ├── status.svg
│   │   ├── status_green.svg
│   │   ├── status_red.svg
│   │   └── User_Circle.svg
│   └── 📁 utils/                      # Client-side utility functions
│       ├── ajaxfetch.js
│       ├── formValidate.js
│       ├── password.js
│       ├── pincode.js
│       └── toast.js
├── 📁 templates/                      # HTML templates - Jinja2 template files for rendering
│   ├── base.html
│   ├── README.md
│   ├── TEMPLATE_GUIDE.md
│   ├── 📁 admin/                      # Admin panel templates
│   │   ├── analytics.html
│   │   ├── dashboard.html
│   │   ├── lot_details.html
│   │   ├── search.html
│   │   ├── spot_details.html
│   │   ├── summary.html
│   │   └── users.html
│   ├── 📁 auth/                       # Authentication templates
│   │   ├── login.html
│   │   └── signup.html
│   ├── 📁 components/                 # Reusable template components
│   │   ├── input.html
│   │   ├── 📁 navigation/             # Navigation components
│   │   │   ├── sidebar.html
│   │   │   └── user_sidebar.html
│   │   └── 📁 notifications/          # Notification components
│   │       └── toast.html
│   ├── 📁 forms/                      # Form templates
│   │   └── form.html
│   └── 📁 user/                       # User interface templates
│       ├── dashboard.html
│       └── summary.html
├── 📁 utils/                          # Server-side utility functions
│   ├── __init__.py
│   └── sanitizer.py
├── 📄 .gitignore
├── 📄 app.py                          # Main App
├── 📄 db.py                           # Db intialization and Shutdown Functions
├── 📄 LICENSE
├── 📄 parkease.db                     # Sqlite Database
├── 📄 README.md
├── 📄 requirements.txt
└── 📄 scheduler.py                    # Scheduler : For Cost AutoUpdation

```

## Unique Features that I Explored
Despite my lack of familiarity with Flask, this was my first time developing a CRUD application in a language other than Node.js, and the experience of Node proved to be very fruitful. As I developed the application, I wanted to add automatic updates to the database and frontend every ten seconds. But I didn't want to do this with WebSockets.

Instead, I developed a straightforward util function `` AjaxFetch.js `` for the frontend and found a scheduler solution for the database updates. Polling is essentially done by repeatedly retrieving the same page and dynamically updating just the UI elements that are required. This method avoided the hassle of configuring real-time sockets and kept things simple.

Here is a simple AjaxFecth like code Snippet :
```js
// We are considering some of the fns 
// as predefined (diffloader) 
const interval = 10000 
// the main ajax fn
const ajax = ()=>{
    fetch(
        window.location.href,{
            headers:{
                  "X-Requested-With": "XMLHttpRequest"
            }
            cache: "no-store"
        }
    )
    .then(response=>{
        if(!response.ok){
        throw new Error(`HTTP error! 
        Status: ${response.status}`);
        }
        return response.text();
    })
    .then(html => {
           diffloader(html)
           // In my project I am extracting the only 
           // part i know can change then if i found a 
           // change i am updating stuff
        })
    .catch(error => {
            console.error("Error checking for updates:", error);
            window.location.reload();
        });
}
setInterval(ajax,interval)
```

Here is a small code example of scheduler:
```py
# just a simple scheduler code by me as an example
# just printing a string
from apscheduler.schedulers.background  import BackgroundScheduler
def update():
    print("Hello World")
scheduler = BackgroundScheduler()
scheduler.add_job(
update,
'interval',
seconds=10,
id='update_job',
replace_existing=True,
max_instances=1,
coalesce=True  
)
scheduler.start()

```

## Models For Db
For the database models and relationship I mainly thought around the given structure and designed a comprehensive system with proper relationships and constraints.

### Database Schema Overview
This WebApp uses an ORM named as SqlAlchemy to simplify database operations

### Core Models

#### 1. **Base Model**
Formed using declartive base function of SqlAlchemy. It helps all the other models to inherit a founational class/Base Class easing the creation of db models using simpler functions like metadata.create_all()

#### 2. **User Model** 
It is the user Model having fileds consisting of user data as follows ``id,FullName,address,pincode,password_hash,email,reservations`` where reservations is a relation with reservation model to link with all user reservation and use UserMixin to auto implement flask login fields

#### 3. **Admin Model**
It is the Admin Model having fileds consisting of user data as follows ``id,username,password_hash,email,parking_lots`` where parking_lots is a relation with ParkingLot model to link with all admin ParkingLot and use UserMixin to auto implement flask login fields

#### 4. **ParkingLot Model**
Represents physical parking locations managed by admins. Each lot has capacity limits (1-50 spots), hourly pricing (1-1000 currency units), location details, and automatic free spot tracking. The model includes revenue generation tracking and enforces unique combinations of pincode, location, and address.

#### 5. **ParkingSpot Model**
Individual parking spaces within a lot. Each spot has a unique identifier, spot number, integer-based status tracking (0=Free, 1=Occupied), and belongs to a specific parking lot. Spots can have multiple reservations over time.

#### 6. **Reservation Model**
Booking records that link users to specific parking spots. Reservations include vehicle number validation (Indian format), automatic cost calculation based on duration and lot rates, and comprehensive time management with start and end times stored as strings.

### Database Relationships

<img src="https://github.com/user-attachments/assets/2bb31369-ebed-407b-9dfb-1cf0cb3a8376" alt="chart" style="height: 700px;" />




## Conclusion
> *I can go on explaning the contoller files, routes,js utils or template files and how they work but i think that will make this document very long*

The WebApp is a fully working app with some of new methods explored by me like  inbuild decorators functions such as @app.before_request, @app.teardown_appcontext.
And it was a good learning experince for me

## Use of AI in the project
The app does not have any AI usage for base functionalities but I have used AI to build some of the Advanced functions like AjaxFetch but with only very little start code by AI 

In Percentages 5% - 7% of the whole app is build using AI

## Use of AI in this Document
Only the mermaid code for flowchart and the ASCII project structure is written by AI
