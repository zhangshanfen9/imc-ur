We share the following artifacts:

- The components of URHunter collecting suspicious undelegated records (Section 4.1 and 4.2)
  - Section 4.1: `/sec4.1-get-ur`
  - Section 4.2: `/sec4.2-get-sus-ur`
- Our measurement data of undelegated records (Section 5), including:
  - A list of all undelegated records
    - including the hosted domain, nameserver, resource data, category (malicious, unknown, correct, and protective), and the reason to be labeled (if it is malicious)
  - A list of malicious traffic related to undelegated records
    - including the related IP address, malware (MD5), alert level, and traffic type.
  - A list of IP addresses related to malicious undelegated records
    - including the IP address, the reason to be labeled, and #vendor that labeled the IP address as malicious

We don't share the following artifacts, and we state our reasons as follows:

- The component identifying the malicious URs (Section 4.3)
  - This component requires specific APIs and tokens to access the services provided by the security vendors that collaborated with us
  - All security vendors authorized their services for this research only and did not allow for any public usage
  - However, we make our identified result available (including the reason for being labeled as malicious). Such information is enough to evaluate our study and conduct further research