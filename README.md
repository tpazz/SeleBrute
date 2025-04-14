# SeleBrute.py

SeleBrute is a Selenium based tool designed for brute forcing form based authentication. Tools like Hydra and Medusa excel in many typical authentication scenarios but often struggle with dynamic tokens present on some websites.

SeleBrute addresses this challenge by simulating real user interactions within a WebDriver, automatically handling dynamic elements such as tokens or CSRF parameters. However, this approach involves a significant trade-off in speed, achieving an average rate of only about 2 password attempts / second in headless mode. Still looking for that free lunch.

> Note: Use this tool responsibly and only with explicit permission from the system owner or within authorized testing environments.

Below is the high level flow of actions SeleBrute performs when attempting online-brute forcing:

<p align="center">
  <img src="https://github.com/user-attachments/assets/d085688f-c06c-4cc0-b038-0be7683f4dca" height="800" />
</p>
