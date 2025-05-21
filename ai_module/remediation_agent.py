def suggest_remediations(df):
    def suggest(row):
        control = row['Control']
        score = row['Score']
        domain = row['Domain']

        if score < 60:
            if domain == "Access Control":
                return "Enforce least privilege and automate quarterly access reviews."
            elif domain == "DevSecOps":
                return "Integrate security scanning tools into your CI/CD pipeline."
            elif domain == "Network Security":
                return "Segment networks and review firewall configurations."
            else:
                return "Review and strengthen controls in this domain."
        elif score < 80:
            return "Review documentation, training, and automation in this area."
        else:
            return "Control performing well. Maintain current processes."

    df['Remediation'] = df.apply(suggest, axis=1)
    return df