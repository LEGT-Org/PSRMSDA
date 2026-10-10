import Swal from 'sweetalert2';

interface ValidationField {
    Value: string;
    Message: string;
}

export const ValidateDiagnosisForm = async (
    CustomerFirstName: string,
    CustomerLastName: string,
    CustomerEmail: string,
    CustomerPhoneNumber: string,
    DeviceType: string,
    DeviceBrand: string,
    DeviceModel: string,
    FaultDescription: string,
): Promise<boolean> => {
    const Fields: ValidationField[] = [
        { Value: CustomerFirstName, Message: 'Customer first name is required.' },
        { Value: CustomerLastName, Message: 'Customer last name is required.' },
        { Value: CustomerEmail, Message: 'Customer email is required.' },
        { Value: CustomerPhoneNumber, Message: 'Customer phone number is required.' },
        { Value: DeviceType, Message: 'Device type is required.' },
        { Value: DeviceBrand, Message: 'Device brand is required.' },
        { Value: DeviceModel, Message: 'Device model is required.' },
        { Value: FaultDescription, Message: 'Fault description is required.' },
    ];

    const MissingField = Fields.find(
        (Field: ValidationField) => !Field.Value.trim()
    );

    if (MissingField) {
        await Swal.fire({
            title: 'Validation Error',
            text: MissingField.Message,
            icon: 'warning',
            confirmButtonText: 'OK',
        });

        return false;
    }

    return true;
};