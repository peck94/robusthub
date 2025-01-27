Domain generation algorithms (DGAs) are frequently used by malware creators to exfiltrate data from their targets, send commands to infected hosts and update the malware itself. A DGA is a pseudo-random generator which creates domain names that can subsequently be registered by the malware authors for command and control purposes. The random seed for this generator is typically some piece of publicly available data, such as the current time in a specific timezone or the timestamp of the latest social media post of a given celebrity, so that the malware and its authors can synchronize the generation of domain names across the world and thus establish reliable communication. DGAs circumvent traditional blacklisting approaches since the number of unique domain names they can generate is either prohibitively large or even theoretically infinite, and once a domain has been disabled, the malware simply moves down the list to the next available one.

DGAs are however subject to an important restriction: they must avoid generating domain names that are likely to already be registered, as this hampers their efficiency and can lead to malfunction. Therefore, DGAs need to tread a fine line: they cannot generate names that are obvious gibberish, as these are easy to detect; but they also cannot generate names that are "too human," since the resulting domain could already be registered.

### Metrics

* **TPR@FPR=$p$.** DGA detection algorithms must be effective at very low false positive rates (FPRs), typically FPR@0.1% or lower, because erroneously disabling a legitimate domain is very disruptive. Hence the true positive rate (TPR) at a given low FPR is the most important metric here, with $p \in \{ 1\%, 0.1\%, 0.01\% \}$ as common choices.
* **AUC.** As with all detectors, DGA classifiers can also be evaluated according to their AUC.
* **F1.** The F1 score is also commonly used to evaluate binary classifiers.

### Threat models

In practice, domain names are rarely (if ever) manually inspected by human beings. Moreover, since the adversaries in this task are malware designers, it is unlikely that there exists a formal threat model that captures all existing and future DGA software. The threat model for this usecase is unspecified, except for the fact that the algorithms must produce textual output resulting in valid domain names as defined by [RFC 1035](https://www.ietf.org/rfc/rfc1035.txt).

### References

* [Down to earth! Guidelines for DGA-based Malware Detection](https://dl.acm.org/doi/pdf/10.1145/3678890.3678913)
* [Towards robust domain generation algorithm classification](https://dl.acm.org/doi/pdf/10.1145/3634737.3656287)
* [ReplaceDGA: BiLSTM-Based Adversarial DGA With High Anti-Detection Ability](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10177739)
* [CharBot: A Simple and Effective Method for Evading DGA Classifiers](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=8756038)
* [An evaluation of DGA classifiers](https://ieeexplore.ieee.org/abstract/document/8621875)
