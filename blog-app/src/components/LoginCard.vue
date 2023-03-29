<template>
    <div class="form-container">
        <h1>Login to your Account</h1>
        <b-form style="width: 70%" @submit="onSubmit" @reset="onReset">
            <b-form-group id="username-group" label="Username:" label-for="username">
                <b-input-group class="mt-0">
                    <template #prepend>
                        <b-input-group-text>
                            <b-icon-person-fill></b-icon-person-fill>
                        </b-input-group-text>
                    </template>
                    <b-form-input id="username" v-model="form.username" placeholder="Username" required></b-form-input>
                </b-input-group>
            </b-form-group>

            <b-form-group id="password-group" label="Password:" label-for="password">
                <b-input-group class="mt-0">
                    <template #prepend>
                        <b-input-group-text>
                            <b-icon-key></b-icon-key>
                        </b-input-group-text>
                    </template>
                    <b-form-input :type="showPassword ? 'text' : 'password'" id="password" v-model="form.password"
                        placeholder="Password" required></b-form-input>
                    <template #append>
                        <b-button :variant="!showPassword ? 'primary' : 'danger'" @click="showPassword = !showPassword">
                            <b-icon :icon="!showPassword ? 'eye-slash' : 'eye'"></b-icon>
                        </b-button>
                    </template>
                </b-input-group>
            </b-form-group>

            <b-form-group id="input-group-4" v-slot="{ ariaDescribedby }">
                <b-form-checkbox-group v-model="form.checked" id="checkboxes-4" :aria-describedby="ariaDescribedby">
                    <b-form-checkbox value="remember">Remember Me</b-form-checkbox>
                </b-form-checkbox-group>
            </b-form-group>
            <p style="margin: 2% 0">Don't have an account? <a @click="$emit('create-account')">Create one</a></p>

            <b-button type="submit" variant="primary">Login</b-button>
        </b-form>
    </div>
</template>

<script>
import { mapActions } from 'vuex';
export default {
    data() {
        return {
            form: {
                username: '',
                password: '',
                checked: [],
            },
            showPassword: false
        }
    },
    methods: {
        ...mapActions({
            login: 'LOGIN_ACTION'
        }),
        onSubmit(event) {
            event.preventDefault()
            // const path = 'http://localhost:5000/api/v1/login';

            var formData = new FormData();
            formData.append('username', this.form.username);
            formData.append('password', this.form.password);

            this.login(formData)
            // axios({
            //     method: 'post',
            //     url: path,
            //     data: formData,
            //     headers: { 'Content-Type': 'multipart/form-data' }
            // })
            //     .then((res) => {
            //         this.msg = res.data;
            //         console.log("API Result: ", this.msg)
            //         if (res.status === 200) {
            //             this.$router.push('/dashboard')
            //         }
            //     })
            //     .catch((error) => {
            //         // eslint-disable-next-line
            //         console.error(error);
            //     });
        },
        onReset(event) {
            event.preventDefault()
            // Reset our form values
            this.form.email = ''
            this.form.username = ''
            this.form.checked = []
        },
    },
}
</script>

<style scoped>
.form-container {
    text-align: left;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    padding: 10% 5%;
    border-radius: 5%;
}
</style>