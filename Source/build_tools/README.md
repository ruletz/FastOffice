<h1>ONLYOFFICE Build Tools</h1>

Welcome to the ```build_tools``` repository! This powerful toolkit simplifies the process of compiling [ONLYOFFICE](https://github.com/ONLYOFFICE) products from source on Linux.

It automatically fetches all the required dependencies and source code to build the latest versions of:

* [Docs (Document Server)](https://www.onlyoffice.com/docs?utm_source=github&utm_medium=cpc&utm_campaign=GitHubBuildTools)  
* [Desktop Editors](https://www.onlyoffice.com/desktop?utm_source=github&utm_medium=cpc&utm_campaign=GitHubBuildTools)  
* [Document Builder](https://www.onlyoffice.com/document-builder?utm_source=github&utm_medium=cpc&utm_campaign=GitHubBuildTools)

**A quick note:** For the most stable and reliable builds, we strongly recommend compiling from the ```master``` branch of this repository.

## **How do I use it on Linux? 🐧**

>This guide has been tested and verified on **Ubuntu 16.04**.

### **Step 1: Install dependencies**

First, let's make sure you have **Python** installed, as it's needed to run the build scripts.

```bash
sudo apt-get install -y python
```

### **Step 2: Build the source code**

Now, you're ready to build the ONLYOFFICE products.

1. **Clone the build_tools repository:**  

    This command downloads the build tools to your machine using Git:
   ```bash
   git clone https://github.com/ONLYOFFICE/build_tools.git
   ```

2. **Navigate to the scripts directory:**  
   ```bash
   cd build_tools/tools/linux
   ```
3. **Run the automation script:**  
   
   This is where the magic happens! Running the script without any options will build all three products: Document Server, Document Builder, and Desktop Editors.  

   ```bash
   ./automate.py
   ```
You can also build ONLYOFFICE products separately. Just run the script with the parameter corresponding to the necessary product. For example, to build *Desktop Editors* and *Document Server*
  ```bash
   ./automate.py desktop server
   ```

**Perfect!** Once the script finishes, you will find the compiled products in the ```./out``` directory.

## **Advanced options & different workflows 🚀**

### **How to use Docker**

If you prefer using Docker, you can build all products inside a container. This is a great way to keep your local system clean.

1. **Create an output directory:**  

   ```bash
   mkdir out
    ```

2. **Build the Docker image:**  

   ```bash
   docker build --tag onlyoffice-document-editors-builder .
   ```

3. **Run the container to start the build:** 
   
   This command mounts your local out directory into the container, so the final build files will appear on your machine. 

   ```bash 
   docker run -v $PWD/out:/build_tools/out onlyoffice-document-editors-builder
    ```

You've done it! The results will be in the ```./out``` directory you created.

## **How to build and run the products separately ▶️**

Don't need everything? You can save time by building only the products you need. Just add the product name as an argument to the script.

### Need just the [Document Builder](https://github.com/ONLYOFFICE/DocumentBuilder)❓
* How to build

  ```bash
  ./automate.py builder
  ```
* How to run
  ```bash
  cd ../../out/linux_64/onlyoffice/documentbuilder
  ./docbuilder
  ```

### Need just the [Desktop Editors](https://github.com/ONLYOFFICE/DesktopEditors)❓

* How to build
  ```bash
  ./automate.py desktop
  ```
* How to run
  ```bash
  cd ../../out/linux_64/onlyoffice/desktopeditors
  LD_LIBRARY_PATH=./ ./DesktopEditors
  ```

### Need just the [Docs (Document Server)](https://github.com/ONLYOFFICE/DocumentServer)❓
* How to build
  ```bash
  ./automate.py server
  ```
* How to run

  Running the Document Server is a multi-step process because it relies on a few background services. Let's break it down step by step. 

#### **Step 1. Set up dependencies**

The Document Server needs a few things to run correctly:

* **NGINX**: Acts as a web server to handle requests.  
* **PostgreSQL**: Used as the database to store information.  
* **RabbitMQ**: A message broker that helps different parts of the server communicate.

Here are the commands to install and configure them.

#### **Install and configure NGINX**

1. Install NGINX  
```bash
sudo apt-get install nginx
```
2. Disable the default NGINX site
```bash
sudo rm -f /etc/nginx/sites-enabled/default
```
3. Set up the new website. To do that create the ```/etc/nginx/sites-available/onlyoffice-documentserver``` file with the following contents:

```bash
map $http_host $this_host {
  "" $host;
  default $http_host;
}
map $http_x_forwarded_proto $the_scheme {
  default $http_x_forwarded_proto;
  "" $scheme;
}
map $http_x_forwarded_host $the_host {
  default $http_x_forwarded_host;
  "" $this_host;
}
map $http_upgrade $proxy_connection {
  default upgrade;
  "" close;
}
proxy_set_header Host $http_host;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection $proxy_connection;
proxy_set_header X-Forwarded-Host $the_host;
proxy_set_header X-Forwarded-Proto $the_scheme;
server {
  listen 0.0.0.0:80;
  listen [::]:80 default_server;
  server_tokens off;
  rewrite ^\/OfficeWeb(\/apps\/.*)$ /web-apps$1 redirect;
  location / {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
  }
}
```

4. Enable the new site by creating a symbolic link  
```bash
sudo ln -s /etc/nginx/sites-available/onlyoffice-documentserver /etc/nginx/sites-enabled/onlyoffice-documentserver
```
5. Restart NGINX to apply the changes  
```bash
sudo nginx -s reload
```
#### **Install and configure PostgreSQL**

1. Install PostgreSQL  
    ```bash
    sudo apt-get install postgresql
    ```

2. Create a database and user. 

    **Note**: The user and password must both be **'onlyoffice'.**  
    ```bash
    sudo -i -u postgres psql -c "CREATE USER onlyoffice WITH PASSWORD 'onlyoffice';"
    sudo -i -u postgres psql -c "CREATE DATABASE onlyoffice OWNER onlyoffice;"
    ```

3. Configure the database:  
    ```bash
    psql -hlocalhost -Uonlyoffice -d onlyoffice -f ../../out/linux_64/onlyoffice/documentserver/server/schema/postgresql/createdb.sql
    ```

Upon that, you will be asked to provide a password for the onlyoffice PostgreSQL user. Please enter the **onlyoffice** password.

#### **Install RabbitMQ**
```bash
sudo apt-get install rabbitmq-server
```

Now that you have all the dependencies installed, it's time to generate server files. 
#### **Step 2. Generate server files**

Before running the server, you need to generate font and theme data.

##### **Generate fonts data**

```bash
cd out/linux_64/onlyoffice/documentserver/
mkdir fonts
LD_LIBRARY_PATH=${PWD}/server/FileConverter/bin server/tools/allfontsgen \
  --input="${PWD}/core-fonts" \
  --allfonts-web="${PWD}/sdkjs/common/AllFonts.js" \
  --allfonts="${PWD}/server/FileConverter/bin/AllFonts.js" \
  --images="${PWD}/sdkjs/common/Images" \
  --selection="${PWD}/server/FileConverter/bin/font_selection.bin" \
  --output-web='fonts' \
  --use-system="true"
```

##### **Generate presentation themes**
```bash
cd out/linux_64/onlyoffice/documentserver/
LD_LIBRARY_PATH=${PWD}/server/FileConverter/bin server/tools/allthemesgen \
  --converter-dir="${PWD}/server/FileConverter/bin"\
  --src="${PWD}/sdkjs/slide/themes"\
  --output="${PWD}/sdkjs/common/Images"
```

#### **Step 3. Run the Document Server services**

All Document Server components run as foreground processes. Thus you need separate terminal consoles to run them or specific tools which will allow to run foreground processes in background mode.

* **Start the FileConverter service:**  
  ```bash
  cd out/linux_64/onlyoffice/documentserver/server/FileConverter
  LD_LIBRARY_PATH=$PWD/bin \
  NODE_ENV=development-linux \
  NODE_CONFIG_DIR=$PWD/../Common/config \
  ./converter
  ```

* **Start the DocService service:**  
  ```bash
  cd out/linux_64/onlyoffice/documentserver/server/DocService
  NODE_ENV=development-linux \
  NODE_CONFIG_DIR=$PWD/../Common/config \
  ./docservice
  ```

## And it's a wrap!  🎉
Congratulations! You have successfully used the ```build_tools``` to compile your desired ONLYOFFICE products from the latest source code. 

Everything is now set up. You can go ahead and run your brand-new, self-compiled ONLYOFFICE applications. 

## Need help or have an idea? 💡

* **🐞 Found a bug?** Please report it by creating an [issue](https://github.com/ONLYOFFICE/build_tools/issues).
* **❓ Have a question?** Ask our community and developers on the [ONLYOFFICE Forum](https://community.onlyoffice.com).
* **💡 Want to suggest a feature?** Share your ideas on our [feedback platform](https://feedback.onlyoffice.com/forums/966080-your-voice-matters).
* **🧑‍💻 Need help for developers?** Check our [API documentation](https://api.onlyoffice.com/?utm_source=github&utm_medium=cpc&utm_campaign=GitHubBuildTools).

---

<p align="center"> Made with ❤️ by the ONLYOFFICE Team </p>
