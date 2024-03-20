<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <header>
        <h1>py_eye</h1>
    </header>
    <section>
        <h2>Description</h2>
        <p>The <strong>py_eye</strong> is a Python script designed to collect comprehensive information from computer systems (CPs) and store this data in a .txt file. Initially, <strong>py_eye</strong> is fully operational on Windows platforms, with partial functionality available on Linux systems.</p>
        <p>Its primary purpose is to facilitate the inventory management of computers, users, MAC addresses, and network connections at the Florianópolis City Hall. By integrating <strong>py_eye</strong> with a Group Policy Object (GPO) script, it will be deployed across all computers, utilizing a JSON link for data handling.</p>
    </section>
    <section>
        <h2>Requirements</h2>
        <li>This script requires Python installed on your system. While it's fully operational on Windows, some features may work on Linux.</li>
        <li>You also need to install the libraries used (netifaces and requests, the other ones are natural libs from python) </li>
        <li>To install netiface you may need to download Microsoft Visual C++ Compilation Tools (<a href=https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/>download link</a>)</li>
    </section>
    <section>
        <h2>How to Use</h2>
        <p>To use <strong>py_eye</strong>, follow these steps:</p>
        <ol>
            <li>Ensure Python is installed on your system.</li>
            <li>Clone the repository or download the script to your computer.</li>
            <li>Execute the script using a terminal or command prompt:</li>
            <pre><code>python main.py</code></pre>
            <li>Review the generated .txt file for the collected information.</li>
        </ol>
    </section>
    <section>
        <h2>Contributing</h2>
        <p>Contributions to <strong>py_eye</strong> are welcome! If you have suggestions or improvements, please fork the repository and submit a pull request.</p>
    </section>
</body>
</html>
