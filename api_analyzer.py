class ApiAnalyzer:
    def __init__(self, URI):
        self.URI = URI

    def detect_amorphous_uri(self):
        P = "Tidy End-point"
        AP = "Amorphous End-point"
        found_AP = 0
        p_count = 0
        ap_count = 0
        amorphus_result_AP = []
        amorphus_result_P = []
        extensions = [".json", ".html", ".pdf", ".txt", ".xml", ".jpg", ".jpeg", ".png", ".gif", ".csv", ".htm", ".zip"]

        for line in self.URI:
            comment = ""
            found_AP = 0

            if "%5F".lower() in line.lower() or "%5F" in line:
                found_AP = 1
                comment += " [underscore found] "

            c = line.strip()[-1]
            if c == '/' or c == '\\':
                found_AP = 1
                comment += " [trailing slash found] "

            for extension in extensions:
                if extension.lower() in line.lower() or extension.upper() in line:
                    found_AP = 1
                    comment += " [extension found] "

            if found_AP == 1:
                ap_count = ap_count + 1
                amorphus_result_AP.append(line.strip() + "\t" + AP + "\t" + comment)
            else:
                p_count = p_count + 1
                amorphus_result_P.append(line.strip() + "\t" + P + "\t" + comment)

        return amorphus_result_AP, amorphus_result_P, p_count, ap_count
