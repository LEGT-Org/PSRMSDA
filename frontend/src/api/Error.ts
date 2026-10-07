export interface ApiValidationError {
    type?: string;
    loc?: (string | number)[];
    msg?: string;
}

const FormatFieldName = (location?: (string | number)[]): string => {

    if (!location || location.length === 0) {
        return 'Request';
    }

    const field = location[location.length - 1];

    if (typeof field !== 'string') {
        return 'Request';
    }

    return field
        .replace(/_/g, ' ')
        .replace(/\b\w/g, (letter) => letter.toUpperCase());
};

export const ParseApiError = async (
    response: Response,
    fallbackMessage: string
): Promise<string> => {

    try {

        const errorData = await response.json();

        if (Array.isArray(errorData.detail)) {

            return errorData.detail
                .map((error: ApiValidationError) => {

                    const field = FormatFieldName(
                        error.loc
                    );

                    return `${field}: ${error.msg}`;
                })
                .filter(Boolean)
                .join('\n');

        }

        if (typeof errorData.detail === 'string') {
            return errorData.detail;
        }

        if (typeof errorData.message === 'string') {
            return errorData.message;
        }

        return fallbackMessage;

    } catch {

        return fallbackMessage;
    }
};