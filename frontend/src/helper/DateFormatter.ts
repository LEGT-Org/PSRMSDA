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


export const FormatDate = (DateValue: string): string => {
    const utcDate = DateValue.endsWith("Z")
        ? DateValue
        : `${DateValue}Z`;

    return new Date(utcDate).toLocaleString("en-PH", {
        timeZone: "Asia/Manila",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: true,
    });
};