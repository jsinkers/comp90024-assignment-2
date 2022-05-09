<script>
    import { useNavigate } from "svelte-navigator";

    const navigate = useNavigate();
</script>

<div class="container">
    <div class="relative flex items-center justify-center flex-col h-full w-full p-2 bg-white bg-opacity-30 rounded-2xl backdrop-filter">
        <span class="relative flex items-center justify-center text-2xl mb-10">Social Engagement</span>
        <p>To explore the social engagement liveability indicator, we have examined trends between socioeconomic studies and interest in election issues</p>
        <p>Our analysis measures socioeconomic status using 2016 ABS data on Socio-Economic Index for Areas (SEIFA) for
            each suburb, and examines the sentiment and number of tweets related to particular election issues. </p>
        <p id="vis-p">Select a visualisation</p>
        <span class="btn-group justify-center items-center">
        <button class="button" on:click={()=>navigate('map')}>Map</button>
        <button class="button" on:click={()=>navigate('chart')}>Chart</button>
    </span>
    </div>
</div>

<style>
    .container {
        @apply h-full w-full;
    }

    .button {
        @apply bg-white border-2 border-blue-300 rounded-2xl p-2 hover:bg-blue-300 hover:text-white hover:border-white;
    }

    .btn-group {
        @apply relative flex items-center justify-center space-x-4 w-1/2;
        text-align: center;
    }

    p {
        margin: 5px;
    }

    #vis-p {
        text-align: center;
    }
</style>
