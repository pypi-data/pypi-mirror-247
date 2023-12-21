<br/>
<h2 align="center">
    <p align="center">
        <img src="img/smce-support-services.png" alt="SMCE Services Support Logo" width="230" height="150">
    </p>
    This extension provides in-platform support for the SMCE services through Voice Atlas.
</h2>
<br/>

# Contents

- [What is it?](#what-is-it)
- [Installation](#installation)
- [Usage](#usage)
- [Licensing](#licensing)

<br/>

### What is it?

The Science Managed Cloud Environment (SMCE) is a managed cloud environment that utilizes commercial Amazon Web Services (AWS) for rapid prototyping and collaboration to accelerate the National Aeronautics and Space Administration (NASA) research.

<br/>

### Installation

**This extension might not be useful at least you are an SMCE user.**

You can use `pip` to install this extension:

```bash
pip install jupyterlab-smceservices
```

or

```bash
git clone https://github.com/Navteca/jupyterlab-smceservices.git
cd jupyterlab-smceservices/
npm install
python -m build
pip install jupyterlab_smceservices-<version>-py3-none-any.whl
```

<br/>
if the installation process runs successfully, check if the extension has been activated:

```
jupyter labextension list
jupyter serverextension list
```

<br/>
If not, you might need to run:

```
jupyter labextension enable --py jupyterlab_smceservices
jupyter serverextension enable --py jupyterlab_smcewervices
```

<br/>

### Usage

Once the extension is installed, you will notice there is a new menu item "Support" which will give you access to the support chat.

<br/>

### Licensing

TBD

<br/>
