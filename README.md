✔ Objectives

Use AWS services, Amazon Lookout for Vision, Kinesis Video Streams (KVS), Lambada functions, and S3 to provide end-end image/video based defect detecting serverless solution:
- Provide a machine learning service to create defect models based on normal/anomaly training images provided by quality inspector; 
- use the model to detect real time image generated by on-site video cameras; 
- notify engineers to fix the defect in real time; 
- help to generate defect reporting; 
- feed back detect result to re-train existing ML models to keep improving them.

✔Use Cases

Use case 1: Mike is a Pre-Production Quality Inspector in a manufacturer. He is in charge of approving or rejecting raw materials with respect to quality standards. On a daily basis, he needs to manually check hundreds or thousands of materials and parts to discover defects, wear (the result of things such as corrosion, erosion, abrasion, chemical processes, or combinations of these factors), and tear.
- He hopes to have a ML solution to provide an automatic inspection.
  
Use case 2: Susan is a During-Production Quality inspector in the same manufacturer. Her job is to conduct inspections of systems and components while production is underway. She uses manuals and checklists provided by the manufacturer to see if components are properly installed (no bolts are missing or improperly installed, etc.) based on scheduled plan on a daily basis. 
- She wants to teach machine to inspect those components automatically at the end of each day.
  
Use case 3: Peter is a project manager.  His responsibilities include generating daily report to aggregate how many quality defects are found by his team’s 5 quality inspectors during production; and based on the report, rearranging resources and redefining project plan. He needs to manually collect raw data from several quality working spreadsheets, remove duplication and make necessary changes, and summarize the aggregation in a final spreadsheet.
- He desires to have an automatic defect collecting and reporting service 

✔Architecture

![image](https://github.com/user-attachments/assets/8885e285-bb23-4547-b954-e43d2698d8ea)





