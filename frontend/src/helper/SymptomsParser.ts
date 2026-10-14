export const parseFaultDescriptions = (text: string): string[] => {
    return text
        .split('\n')
        .map(line => line.replace(/^[-•]\s*/, '').trim())
        .filter(Boolean);
};


export const FormatAlertType = (Type: string): string => {
    
    return Type
        .toLowerCase()
        .split('_')
        .map((Word) => Word.charAt(0).toUpperCase() + Word.slice(1))
        .join(' ');
};
