<template>
    <div :class="['message', sender === 'me' ? 'me' : 'chatbot']">
        <p>{{ message }}</p>
    </div>
</template>

<script>
export default {
    props: {
        sender: String,
        message: String
    }
}
</script>

<style scoped>
.message {
    max-width: 60%;
    padding: 0.75rem 1rem;
    border-radius: 16px;
    word-wrap: break-word;
}

.me {
    align-self: flex-end;
    background-color: #dcf8c6;
}

.chatbot {
    align-self: flex-start;
    background-color: #ececec;
}
</style>