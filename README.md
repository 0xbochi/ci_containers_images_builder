# ci_containers_images_builder

Builds container images with GitHub Actions and pushes them to Docker Hub.

## Images


Table generated automatically by the CI after each build, do not edit by hand.

<!-- IMAGES:START -->
<!-- IMAGES:END -->

## Layout

```
<repo>/            # = a Docker Hub repository  (<namespace>/<repo>)
  <tag>/           # = a tag of that repository
    Containerfile  # required, this folder is the build context
    ...            # any files the Containerfile COPYs
```

`i686-elf-toolchain/gcc-15.2.0/Containerfile` is pushed as
`<namespace>/i686-elf-toolchain:gcc-15.2.0`.

The same image with another tag is just another folder next to it.
Docker Hub creates the repository on the first push.

Only folders changed by a push are rebuilt (everything is rebuilt if the
workflow or the scripts change, or via manual dispatch). Pull requests build
without pushing.

## Setup (once)

GitHub → Settings → Secrets and variables → Actions

- Variable `DOCKERHUB_USERNAME`: the Docker Hub namespace (`lbochi`)
- Secret `DOCKERHUB_TOKEN`: Docker Hub access token with Read & Write

GitHub → Settings → Actions → General → Workflow permissions: allow
"Read and write permissions" (the CI commits the updated table).
