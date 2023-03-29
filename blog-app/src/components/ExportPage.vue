<template>
    <div>
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Export Data</h5>
                <p class="card-text">Export your data in either PDF or CSV format</p>
                <div class="d-flex justify-content-between">
                    <a href="#" @click="updateFlag(1)" class="btn btn-primary">Export as PDF</a>
                    <a href="#" @click="updateFlag(0)" class="btn btn-primary">Export as CSV</a>
                </div>
            </div>
        </div>
        <div v-if="(flag === 1)" id="divToPrint" class="mt-5">
            <h4>Post Details</h4>
            <div class="table-responsive">
                <table class="table table-bordered" @click="printDocument()">

                    <thead>
                        <tr>
                            <th>Post ID</th>
                            <th>Post Author ID</th>
                            <th>Post Caption</th>
                            <th>Posted On</th>
                            <th>No. of Likes</th>
                            <th>Author Username</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="blog in mutableBlogDetails" :key="blog.blog_id">
                            <td>{{ blog.blog_id }}</td>
                            <td>{{ blog.author_id }}</td>
                            <td>{{ blog.caption }}</td>
                            <td>{{ blog.created_at }}</td>
                            <td>{{ blog.likeCount }}</td>
                            <td>{{ blog.author }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-if="(flag === 0)" class="mt-5 text-center">
            <h2>Export data to CSV</h2>
            <button class="btn btn-primary" @click="exportData">Download CSV file</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {excelParser} from '../excel-parser'
import pdfMake from 'pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';
import htmlToPdfmake from 'html-to-pdfmake';
export default {
    props: {
        blogDetails: {
            type: Array,
            required: true
        },
    },
    data() {
        return {
            flag: -1,
            likesCount: null,
            mutableBlogDetails: this.blogDetails
        }
    },

    methods: {
        updateFlag(data) {
            this.flag = data
        },

        async getLikes() {
            await axios.get('http://localhost:5000/api/v1/likes-count/all-blogs', {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then(res => {
                    this.likesCount = res.data.data
                })
                .catch(err => {
                    console.log(err)
                })
        },
        getLikeCount() {
            for (let i = 0; i < this.blogDetails.length; i++) {
                for (let j = 0; j < this.likesCount.length; j++) {
                    if (this.blogDetails[i].blog_id === this.likesCount[j].blog_id) {
                        this.mutableBlogDetails[i].likeCount = this.likesCount[j].likes_count
                    }
                }
            }
        },
        printDocument() {
            const pdfTable = document.getElementById('divToPrint');
            var html = htmlToPdfmake(pdfTable.innerHTML);

            const documentDefinition = { content: html };
            pdfMake.vfs = pdfFonts.pdfMake.vfs;
            pdfMake.createPdf(documentDefinition).open();

        },
        exportData() {
            let copyBlogDetails = this.blogDetails
            for (let i = 0; i < copyBlogDetails.length; i++) {
                delete copyBlogDetails[i].image
            }
            excelParser().exportDataFromJSON(this.blogDetails, null, null);
        },
    },

    async created() {
        await this.getLikes()

        this.getLikeCount()
    }
}
</script>

<style></style>