<script lang="ts">
import axios from "axios";
import 'bootstrap';
import 'bootstrap/scss/bootstrap.scss';

const baseUrl = import.meta.env.VITE_API_ENDPOINT
export default {
    data() {
        return {
            mysfits: [],
            filterOptionsList: {
              "categories": [
           {
             "title": "Good/Evil",
             "selections":  [
               "Good",
               "Neutral",
               "Evil"
             ]
           },
           {
             "title": "Law/Chaos",
             "selections":  [
               "Lawful",
               "Neutral",
               "Chaotic"
             ]
           }
         ]
      }
    }
  },
  methods: { 
    getAllMysfits: function() {
        axios.get(baseUrl+'/mysfits').then((response) => {
        this.mysfits = response.data
        this.$forceUpdate()
      })
    },
    getFilteredMysfits: function(attributeName,attributeValue) {
      const attribute=attributeName.replace("/","")
      axios.get(baseUrl+"mysfits?filter="+attribute+"&value="+attributeValue).then((response) => {
        this.mysfits = response.data
      })
      this.$forceUpdate()
    }  
  },
  beforeMount() {
    this.getAllMysfits()
  }
}
</script>

<template>
  <nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
    <div id="filterMenu" v-for="category in filterOptionsList.categories">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0"></ul>
      <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#!" role="button">{{category.title}}</a>
            <div class="dropdown-menu" >
              <button class="dropdown-item" v-for="selection in category.selections" @click="getFilteredMysfits(category.title, selection)">{{selection}}</button>
            </div>
      </li>
     
    </div>
    <li class="nav-item " >
            <button type="button" class="btn btn-success" @click="getAllMysfits()">View All</button>
    </li>
  </div>
  </nav>
  <div class="container">
      <div id="mysfitsGrid" class="row">
          <div class="col-md-4 border border-warning" v-bind:key="mysfits" v-for="mysfit in mysfits">
              <br>
              <p align="center">
                <strong> {{mysfit.Name}}</strong>
                <br>
                <img :src="mysfit.ThumbImageUri" :alt="mysfit.Name">
              </p>
              <p>
                <br>
                <b>Species:</b> {{mysfit.Species}}
                <br>
                <b>Age:</b> {{mysfit.Age}}
                <br>
                <b>Good/Evil:</b> {{mysfit.GoodEvil}}
                <br>
                <b>Lawful/Chaotic:</b> {{mysfit.LawChaos}}
              </p>
          </div>
        </div>
      </div>
</template>

<style scoped>
  @import "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css";

  li { list-style-type: none; }

  nav {
  width: 33%;
  font-size: 15px;
  text-align: right;
  margin-top: 2rem;
}
</style>