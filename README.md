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


✔Defects detected in this project

1.  Anomaly in raw material
   
![image](https://github.com/user-attachments/assets/d232fff6-e560-42f5-af15-8825b497d7df)

2. missing component or improperly installed component

![image](https://github.com/user-attachments/assets/42ca5293-7c4b-4dbc-b94e-3ca715943e7b)


✔steps to run the project
1. train and test 2 models, one for anormaly in raw material, and the other is for missing component/improperly installed component
   
   (1) upload training and testing images from data in AWS Lookout for Vision
   ![image](https://github.com/user-attachments/assets/def93eb7-8a0f-4d65-b6c6-93118f6d3e29)


   (2) generate data model and test it
    ![image](https://github.com/user-attachments/assets/ed438c1d-7e40-4f01-a484-2f7406be36a5)


2. deploy 2 lambda functions, one is triggered by S3 to call data model (in this project is calling material anormaly model); and the other is triggered by SQS to process anormaly message

3. load a new material image to S3 to trigger the process automatically
