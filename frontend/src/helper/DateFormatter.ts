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
    return new Date(DateValue).toLocaleString();
};