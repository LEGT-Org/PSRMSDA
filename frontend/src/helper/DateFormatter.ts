export const FormatServiceRequestDate = (createdAt: string): string => {

    return new Date(createdAt).toLocaleDateString(
        'en-US',
        {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
        }
    );
    
};


export const FormatDate = (value: string): string => {
    const utcDate = value.endsWith("Z")
        ? value
        : `${value}Z`;

    const date = new Date(utcDate);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return new Intl.DateTimeFormat("en-PH", {
        month: "short",
        day: "2-digit",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
        timeZone: "Asia/Manila",
    }).format(date);
};