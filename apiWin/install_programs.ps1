function get-info-programs {

    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; 
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); Find-Package -Provider chocolatey | findstr /c:"mysql", /c:"python", /c:"pip"


    $python_version = &{python -V} 2>&1

    $pip_version = &{pip -V} 2>&1

    $mysql_version = &{mysql -V} 2>&1

   

    if($python_version -is [System.Management.Automation.ErrorRecord]) {

        echo $python_version.Exception.Message

        echo Y | choco install python --pre
       

    }

    else {

        echo $python_version
    }

    if($pip_version -is [System.Management.Automation.ErrorRecord]) {

        echo $pip_version.Exception.Message

         echo Y | choco install pip v1.2.0
         

    }

    else {

        echo $pip_version

    }

    if($mysql_version -is [System.Management.Automation.ErrorRecord]) {

        echo $mysql_version.Exception.Message

         echo Y | choco install mysql --force
         echo Y | choco install mysql-python

         #ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';


    }


    else {

        echo $mysql_version

    }

}

get-info-programs