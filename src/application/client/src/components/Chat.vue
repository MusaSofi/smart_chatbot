<script>
import ChatMessage from './ChatMessage.vue'

export default {
  components: {
    ChatMessage
  },
  data() {
    return {
      messages: [
        { sender: 'chatbot', message: 'Hello! How can I assist you today?' }
      ],
      newMessage: '',
      loading: false
    }
  },
  created() {
    if (!localStorage.getItem('user_id')) {
      const uuid = crypto.randomUUID();
      localStorage.setItem('user_id', uuid);
    }
  },
  methods: {
    sendMessage() {
      const text = this.newMessage.trim();
      if (text) {
        this.messages.push({ sender: 'me', message: text });
        this.$nextTick(this.scrollToBottom);
        this.loading = true;

        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            "user_id": localStorage.getItem('user_id'),
            "question": this.newMessage
          })
        };
        console.log(requestOptions);

        fetch('http://localhost:5000/ask', requestOptions)
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            this.messages.push({ sender: 'chatbot', message: data.answer });
          })
          .catch(error => {
            console.error('Error fetching chatbot response:', error);
            this.messages.push({ sender: 'chatbot', message: 'Oops! Something went wrong. Please try again later.' });
          })
          .finally(() => {
            this.loading = false;
            this.$nextTick(this.scrollToBottom);
          });

        this.newMessage = '';
      }
    },
    scrollToBottom() {
      const el = this.$refs.chatBox
      if (el) {
        el.scrollTop = el.scrollHeight
      }
    }
  }
}
</script>

<template>
  <div class="chat-container">
    <div class="chat-wrapper">
      <div class="chat-header">Unichat</div>
      <div class="chat-box" ref="chatBox">
        <ChatMessage v-for="(msg, index) in messages" :key="index" :sender="msg.sender" :message="msg.message" />
      </div>
      <div v-if="loading" class="typing-indicator">
        <div class="spinner"></div>
      </div>
      <div class="chat-input">
        <input v-model="newMessage" @keyup.enter="sendMessage" type="text" placeholder="Type a message..." />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 400px;
  min-height: 70vh;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  box-sizing: border-box;
  z-index: 1000;
}

.chat-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 70vh;
  border: 3px solid #42b983;
  border-radius: 12px;
  background-color: #ffffff;
  overflow: hidden;
}

.chat-header {
  background-color: #42b983;
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid #38a374;
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background-color: #f9f9f9;
}

.chat-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid #ddd;
  background-color: #fff;
}

.chat-input input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.chat-input button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: none;
  background-color: #42b983;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #36976b;
}

.typing-indicator {
  display: flex;
  justify-content: center;
  /* Center horizontally */
  align-items: center;
  background-color: #f9f9f9;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #42b983;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>