<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/build-aau/lcabyg_web_api_doc">
    <img src="doc/LOGO_graphic_small.png" alt="Logo" width="" height="200">
  </a>

# LCAbyg Web API v.1.0 </div>

### About
Documentation, examples, and use cases of the LCAby Web API.

Please be aware that the scope of underlying software architecture is broader than the LCAbyg Web API.


### Installation
1. Get a free API_KEY at [https://api.lcabyg.dk/](https://api.lcabyg.dk/ "https://api.lcabyg.dk/")
2. Clone the repo
```sh
   git clone https://github.com/build-aau/lcabyg_web_api_doc.git
   ```
2. Enter your USERNAME and an API_KEY in the example.py or example_explanation.py 
```sh
   USERNAME = 'INSERT YOUR USERNAME'
   API_KEY = 'INSERT YOUR API KEY'
   ```
3. Based on the login, generate and api access TOKEN that is then used for authentication for all API calls.
4. Before sending a job, ensure your json projects are compatible with [LCAbyg JSON standard](https://www.lcabyg.dk/da/usermanual/brugervejledning-andre-vaerktojer/ "https://www.lcabyg.dk/da/usermanual/brugervejledning-andre-vaerktojer/"). 


### Documentation
- api.md
- csv.md
- Error messages are located in the output JSON data, "extra_output." We are currently working on improving the 
debug-functionality and provide more user-friendly error messages. 

### Examples
- [example.py](example.py) for using the python packages lcabyg_web_api_py and sbi_web_api_py. In the future, these will be Python libraries.
- [example_explanation.py](example_explanation.py) step-by-step explanation of the LCAbyg Web API. 


### License
Distributed under the BSD 2-Clause License. See [LICENSE.md](doc/LICENSE.md) for more information. 


### Contribution
If you have a suggestion that would make this better, you are welcome to [create a pull request](https://github.com/build-aau/parmesan/pulls").


### Projects using the LCAbyg Web API
- [postman configuration](https://github.com/3dbyggeri/LCAbyg_WebAPI_DocumentationAndExamples "https://github.com/3dbyggeri/LCAbyg_WebAPI_DocumentationAndExamples").  Thanks to Tore Hvidegaard and 3dbyggeri danmark ApS.
- Sensitivity analyse (WIP). Developed by Lærke Vejsnæs during her masters thesis spring 2023 [lhv@build.aau.dk](mailto:lhv@build.aau.dk). 

If you have a project that uses the LCAbyg Web API, we would love to feature your project here and on the LCAbyg Web API website. 
Contact Christian Grau Sørensen [cgs@build.aau.dk](mailto:cgs@build.aau.dk)


