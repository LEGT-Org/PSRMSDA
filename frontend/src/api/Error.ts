import Swal from "sweetalert2";


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
            const FirstError = errorData.detail[0] as ApiValidationError | undefined;

            if (FirstError) {
                const Field = FormatFieldName(FirstError.loc);
                return `${Field}: ${FirstError.msg ?? fallbackMessage}`;
            }

            return fallbackMessage;
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


export const HandleApiError = async (
    Response: Response,
    FallbackMessage: string
): Promise<void> => {
    
    const Message = await ParseApiError(
        Response,
        FallbackMessage
    );

    await Swal.fire({
        title: 'Error!',
        text: Message,
        icon: 'error',
        confirmButtonText: 'OK',
        customClass: {
            confirmButton: 'error-button'
        }
    });
};