import Swal from 'sweetalert2';

export const HandleSuccess = async (
    Message: string,
    Title: string = 'Success!'
): Promise<void> => {
    await Swal.fire({
        title: Title,
        text: Message,
        icon: 'success',
        confirmButtonText: 'OK',
        timer: 2000,
        timerProgressBar: true,
    });
};