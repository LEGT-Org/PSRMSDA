export const parseFaultDescriptions = (text: string): string[] => {
    return text
        .split('\n')
        .map(line => line.replace(/^[-•]\s*/, '').trim())
        .filter(Boolean);
};