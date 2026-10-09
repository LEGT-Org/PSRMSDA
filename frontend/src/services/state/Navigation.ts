import { ref } from "vue";


export const ShowNavigation = ref<boolean>(false);


export const ToggleNavigation = (): void => {
    ShowNavigation.value = !ShowNavigation.value;
};

export const CloseNavigation = (): void => {
    ShowNavigation.value = false;
};