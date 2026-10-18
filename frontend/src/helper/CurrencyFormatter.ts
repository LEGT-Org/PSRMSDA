export const FormatCurrency = (
    value: number | string | null,
): string => {
    if (value === null) {
        return '—';
    }

    return new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP',
    }).format(Number(value));
};
