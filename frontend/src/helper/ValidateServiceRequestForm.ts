export const validateDiagnosisForm = (
    CustomerFirstName: string,
    CustomerLastName: string,
    CustomerEmail: string,
    CustomerPhoneNumber: string,
    DeviceType: string,
    DeviceBrand: string,
    DeviceModel: string,
    FaultDescription: string,
): boolean => {

    if (!CustomerFirstName.trim()) {
        alert('Customer first name is required.');
        return false;
    }

    if (!CustomerLastName.trim()) {
        alert('Customer last name is required.');
        return false;
    }

    if (!CustomerEmail.trim()) {
        alert('Customer email is required.');
        return false;
    }

    if (!CustomerPhoneNumber.trim()) {
        alert('Customer phone number is required.');
        return false;
    }

    if (!DeviceType.trim()) {
        alert('Device type is required.');
        return false;
    }

    if (!DeviceBrand.trim()) {
        alert('Device brand is required.');
        return false;
    }

    if (!DeviceModel.trim()) {
        alert('Device model is required.');
        return false;
    }

    if (!FaultDescription.trim()) {
        alert('Fault description is required.');
        return false;
    }

    return true;
};