<template>
  <img v-if="s3FileId" :src="imageUrl" class="smallFundIcon" />

</template>
<script>

import commonApi from '@/api/common'
export default {
  name: 's3Image',
  props: {
    s3FileId: {
      type: String,
      default: () => ""
    }
  },
  data() {
    return {
      imageUrl:'',
    }
  },

  mounted() {
    this.loadImage(this.s3FileId)
  },
  methods: {
    async loadImage(s3FileId) {
      try {
        //
        let imageUrL = await commonApi.manageS3SelectFileVueBlob(s3FileId)

        this.imageUrl = imageUrL
      } catch (error) {
        console.error('Error loading image:', error);
      }
    },

  },
  beforeDestroy(){
    if (this.imageUrl) {
      URL.revokeObjectURL(this.imageUrl);
    }

  },


}
</script>

<style lang="scss" scoped>
.smallFundIcon {
  width: 30px;
  height: 30px;
  vertical-align: middle;
}
</style>
