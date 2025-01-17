## Make Chart Creation for Trends Less Tedious

If you're using EBO BMS software, you’re likely familiar with the tedious process of creating hundreds (or even thousands) of charts from trends. This tool is here to save you from that monotony, making the task much quicker and easier.

You can download the .exe version or build it yourself—whichever you prefer. The setup process is straightforward, and the steps are outlined below:

### What You’ll Need to Provide:

1. **File Name** – Self-explanatory.
2. **EBO Version** – Works with version 6 or later.
3. **Analog and Binary Trend Paths** – Relative to your EBO system.
4. **Trend Names** – You can copy and paste these directly from your EBO software.

## Download the Latest Version:

> [Latest version in zip file](https://github.com/synth-me/Chart-Replicator/releases/tag/v1.0.0)

---------------------------------------

## Tutorial

### How to Use

You can use either the automatic fill or manual fill method.

#### Automatic Fill

In order to use auto fill your project must follow a specific folder structure, you can try the auto-fill mode. We used the pattern our team uses, so be aware of it.

![image](https://github.com/user-attachments/assets/a95c7929-8746-4239-94c4-a6d82bc11b7f)


After setting this up, export it, search using the software, and load it into the replicator by clicking the button **Use this file**.

![image](https://github.com/user-attachments/assets/0cefffe4-b46d-4b25-a0fc-30f7ff5802e9)


------------------------

### Creation Process

If you used the automatic fill method, most of your work is done. If not, or if you want to make changes to the final export, keep reading.

#### File Name

The **File Name** will be the name of the output file. By default, it's the current date and time. This file will be stored in the **./output** folder.

![image](https://github.com/user-attachments/assets/20e21fe6-d534-476a-852c-045c7dbbbfe1)


#### EBO Version

Next is the **EBO Version** of the output file. If you used automatic fill, it will match the version of the base file you chose. Otherwise, it defaults to version 5.

![image](https://github.com/user-attachments/assets/4a6abf0f-f556-45f9-a989-23b71f17eafe)


#### Server Path

The **Server Path** is usually "Server 1" or "Server" by default in most EBO versions. This is useful if you’re applying the output file in a non-local environment.

![image](https://github.com/user-attachments/assets/9871b1a6-4e69-4d39-b4d6-5d41109d4b01)


#### Modbus Checkbox

The **Modbus Checkbox** is crucial. If you’re placing your charts inside a Modbus device, ensure this checkbox is checked. Otherwise, the elements won't be compatible, and the output file won’t work. From version 6 and above, Modbus and standard elements are the same, so the software handles this for you.

![image](https://github.com/user-attachments/assets/0d0f6be3-f73a-47d5-9c77-040b0537e631)


#### Trend Paths

This is the most critical part. If you’re manually inserting trend paths, ensure you don’t mess them up. Check the **References** section in your folders and copy the paths exactly. This is where the automatic fill does most of its work.

![image](https://github.com/user-attachments/assets/c1ce9933-2ca5-40d1-a524-67632cf8297f)


If everything is correct, click the **Build** button. If you want to customize colors or formatting, use the **Config Display Type** button.

![image](https://github.com/user-attachments/assets/8d391f90-2bed-4d56-8606-60de44c7bb23)


#### Configuring Display Type

When configuring the display type, you can choose how the chart will appear to users and set its color (default is red, style is Line). At the bottom, there’s an option to replicate one configuration to the rest. In the example, the first position (0) was replicated to the other points.

![image](https://github.com/user-attachments/assets/72d6ace3-9710-4548-982c-b0f88d0c224c)

![image](https://github.com/user-attachments/assets/4b2a2ede-7813-439c-b578-1788c7fc7fec)

![image](https://github.com/user-attachments/assets/adb331b7-d087-4ee8-adbd-20476675ae7e)

After completing these steps, check your **./output** folder for the file. Import the XML back into EBO, and you should see something like this:

![image](https://github.com/user-attachments/assets/5a447189-9b1d-4d43-bfcd-5ea4b6dba3d0)

----------------------------------

## It’s Done! You’ve Easily Overcome Boredom!
