export function validateTodo(todo) {
    const errors = {};
    const title = todo.title ? todo.title.trim() : "";
    const description = todo.description ? todo.description.trim() : "";

    if (!title) {
        errors.title = "Tieu de cong viec khong duoc de trong.";
    } else if (title.length > 120) {
        errors.title = "Tieu de cong viec toi da 120 ky tu.";
    }

    if (description.length > 1000) {
        errors.description = "Mo ta cong viec toi da 1000 ky tu.";
    }

    return errors;
}
