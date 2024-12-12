
<h1  align="center" style='font-size:50px; '>Post Hub WebSite</h1>

<h2 align="center" style='font-size:30px'>
This is a Simple Website for posts and news That allow the users to read and create posts
</h2>
<p align="center">
<img src="https://th.bing.com/th/id/R.bde2069143dd5c9da9632d2d32f65fbd?rik=HyJf1kgAzFk8dA&pid=ImgRaw&r=0" height="80px" width="120px">
<img src="https://th.bing.com/th/id/OIP.nsOfGAba5hOGx1kkyQAJOwAAAA?rs=1&pid=ImgDetMain" height="80px" width="120px">
<img src="https://cosasdedevs.com/media/posts/photos/realizar-busquedas-con-django-rest-framework.jpg" height="80px" width="120px">
<img src="https://th.bing.com/th/id/OIP.LFX-qeDrQppQplmd6sjaqwAAAA?rs=1&pid=ImgDetMain" height="80px" width="120px">
<img src="https://th.bing.com/th/id/R.e10b9c4d55b6a7e0cb0588bda75ae1fb?rik=ms%2fwgCI1AgiHKA&pid=ImgRaw&r=0" height="80px" width="120px">
<img src="https://th.bing.com/th/id/R.20cfba0b3c95d1405f395462d917b03f?rik=Jwwyt6qPt93b7g&riu=http%3a%2f%2fnetloid.com%2fwp-content%2fuploads%2f2015%2f07%2fnetloid_postgresql.png&ehk=tFw89WZhW06yEW6ZzE13y%2brY3AO8T%2f5w%2f34c%2bM18PJ8%3d&risl=&pid=ImgRaw&r=0" height="80px" width="120px">
<img src="https://th.bing.com/th/id/OIP.i_07bGITzqzK3TqK9HVfdQHaEK?rs=1&pid=ImgDetMain" height="80px" width="120px">
<img src="https://th.bing.com/th/id/OIP.ItRoLH-y1QFVBB2GfPgOwQHaD4?rs=1&pid=ImgDetMain" height="80px" width="120px">
<img src="https://th.bing.com/th/id/OIP.eqye8qb-Y9cZca36f_dpWwHaEW?rs=1&pid=ImgDetMain" height="80px" width="120px">
<img src="https://th.bing.com/th/id/R.7448044342419709f7db743f8b4b29b2?rik=4%2bbbyMMG839%2b2w&pid=ImgRaw&r=0" height="80px" width="120px">

</p>


# DEMO : Simple Intro With main part of website
<br>


<img src="./docs/INTRO.gif" max-width="300" style="width:100%;max-width:700px"/>
<br><br>

## Swagger Page

<img src="./docs/img1.png" max-width="300" style="width:100%;max-width:350px"/>
<img src="./docs/img2.png" max-width="300" style="width:100%;max-width:350px"/>

<br><br>

# Database Schema

### the provided schema is the main database design of the project based on the models we have used in django project.


<img src="./docs/dbmap.svg" max-width="300" style="width:100%;max-width:1000px"/>

<br>

### Online Database Schema on This [Link](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=exported_from_idea.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1PcFByIyC-XnPf3vJ5RuUefoIvGKYrago%26export%3Ddownload)

<br>


# Installation

## 1 .Install Docker 
<h3> For Install Docker in linux or windows use this  <a href='https://docs.docker.com/desktop/setup/install/linux/'>link</a> </h3> 

<br>

## 2. Get The project

### for get the project just clone it from Github or you can use the below code
#### Just copy and past in terminal or CMD 

``` bash
git clone https://github.com/maryus1991/ADV_Blog.git
```

## 3. Start The project 
### For setup and Start the project just run the Below code in terminal or CMD

``` bash
docker compose up --build -d 
```
#### its may take a time to build and run the project 
#### NOTE : Run This code in the directory the cloned the project
 
<br><br>

## 4.Setup The Project
<br>

### First you need to migrate and by run migrate command project database will setup
```bash
docker compose exec blog sh -c 'python manage.py makemigrations'
```
```bash
docker compose exec blog sh -c 'python manage.py migrate'
```

### Then create the admin user for setup default setting for site
```bash
docker compose exec blog sh -c 'python manage.py createsuperuser'
```
### NOTE: After running the command you should enter email and password 

<br>

### 5.Setup the Default Information

#### First you Should to run the following command for create test posts

```bash
docker compose exec blog sh -c 'python manage.py fake_blog enter@your.email'
```
#### NOTE: Enter your email , replace enter@your.email with your email

<br>

#### Secund you should enter the admin page in the following link  
##### Enter the link to your browser 

```url
localhost:8000/admin/SiteSetting/sitesetting/add/
```

<img src="./docs/image.png" max-width="300" style="width:100%;max-width:350px"/>

#### As you see in the above image  you should enter this kind of information 

<br>
<hr>

### And finally you should see the page in the following link
<br>

<img src="./docs/image copy.png" max-width="300" style="width:100%;max-width:350px"/>
<br>

```
localhost:8000/
```

<br><br>

# Contact
<p style='font-size:20px'> I write all part of the project <br> For contact me just mail me at : <a href='mailto:maryus19915123@gmail.com'> maryus19915123@gmail.com </a> <br> </p>

<br><br>

# License
[MIT](https://choosealicense.com/licenses/mit/)

# Bugs
Feel free to let me know if something needs to be fixed. or even any features seems to be needed in this repo.