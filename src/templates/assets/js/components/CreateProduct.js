import React, {useState} from 'react';
import TagsInput from 'react-tagsinput';
import 'react-tagsinput/react-tagsinput.css';
import Dropzone from 'react-dropzone'
import Axios from 'axios';


const CreateProduct = (props) => {
    const [form, setForm] = useState({
        title:"",
        sku: "",
        description:""
    })
    const [base64Strings, setBase64Strings] = useState([]);

    const [productVariantPrices, setProductVariantPrices] = useState([])

    const [productVariants, setProductVariant] = useState([
        {
            option: 1,
            tags: []
        }
    ])
    const handleAddClick = () => {
        // return only id
        let all_variants = JSON.parse(props.variants.replaceAll("'", '"')).map(el => {
            return el.id
        })
        let selected_variants = productVariants.map(el => el.option);
        let available_variants = all_variants.filter(entry1 => !selected_variants.some(entry2 => entry1 == entry2))
        console.log(all_variants.filter(entry1 => !selected_variants.some(entry2 => entry1 == entry2)))
        setProductVariant([...productVariants, {
            option: available_variants[0],
            tags: []
        }])
    };
    console.log({productVariants})
    // handle input change on tag input
    const handleInputTagOnChange = (value, index) => {
        let product_variants = [...productVariants]
        product_variants[index].tags = value
        setProductVariant(product_variants)

        checkVariant()
    }

    // remove product variant
    const removeProductVariant = (index) => {
        let product_variants = [...productVariants]
        product_variants.splice(index, 1)
        setProductVariant(product_variants)
    }

    // check the variant and render all the combination
    const checkVariant = () => {
        let tags = [];

        productVariants.filter((item) => {
            tags.push(item.tags)
        })
variants: [
    {
        "option": 1,
        "tags": ["",""]
    }
]
        setProductVariantPrices([])

        getCombn(tags).forEach(item => {
            setProductVariantPrices(productVariantPrice => [...productVariantPrice, {
                title: item,
                price: 0,
                stock: 0
            }])
        })

    }

    // combination algorithm
    function getCombn(arr, pre) {
        pre = pre || '';
        if (!arr.length) {
            return pre;
        }
        let ans = arr[0].reduce(function (ans, value) {
            return ans.concat(getCombn(arr.slice(1), pre + value + '/'));
        }, []);
        return ans;
    }

    let saveProduct = (event) => {
        event.preventDefault();
    
        const headers = {
            'Content-Type': 'application/json',
        };
    
        const productObj = {
            product_info: form,
            variants: productVariants,
            product_variant_prices: productVariantPrices,
            files: base64Strings
        };
    
        const data = JSON.stringify(productObj);
    
        Axios.post("http://127.0.0.1:8000/product/create/all", data, { headers: headers })
            .then((resp) => {
                console.log(resp);
            })
            .catch((error) => {
                console.log("Product create error:", error);
            });
    };
    
    

    const handleOnChange = (e) => {
        // console.log(e.target.name, e.target.value)
        let label = e?.target?.name
        let value = e.target.value
        setForm((prev)=> ({...prev, [label]: value}))
    }
    const handleFileInputChange = (event) => {
        const files = event.target.files;
    
        if (files.length > 0) {
          const newBase64Strings = [];
    
          Array.from(files).forEach((file) => {
            const reader = new FileReader();
    
            reader.onloadend = () => {
              const base64String = reader.result;
              newBase64Strings.push(base64String);
    
              if (newBase64Strings.length === files.length) {
                setBase64Strings(newBase64Strings);
              }
            };
    
            reader.readAsDataURL(file);
          });
        }
      };
    
    return (
        <div>
            <section>
                <form className="row" onSubmit={saveProduct} >
                    <div className="col-md-6">
                        <div className="card shadow mb-4">
                            <div className="card-body">
                                <div className="form-group">
                                    <label htmlFor="">Product Name</label>
                                    <input type="text" placeholder="Product Name" className="form-control" name='productName' required  onChange={handleOnChange} />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="">Product SKU</label>
                                    <input type="text" placeholder="Product Name" className="form-control" name='productSKU' required onChange={handleOnChange} />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="">Description</label>
                                    <textarea id="" cols="30" rows="4" className="form-control" name='description' required onChange={handleOnChange} ></textarea>
                                </div>
                            </div>
                        </div>

                        <div className="card shadow mb-4">
                            <div
                                className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 className="m-0 font-weight-bold text-primary">Media</h6>
                            </div>
                            <div className="card-body border">
                                {/* <Dropzone onDrop={acceptedFiles => handleFileInputChange(acceptedFiles)}>
                                    {({getRootProps, getInputProps}) => (
                                        <section>
                                            <div {...getRootProps()}>
                                                <input {...getInputProps()} type='file' />
                                                <p>Drag 'n' drop some files here, or click to select files</p>
                                            </div>
                                        </section>
                                    )}
                                </Dropzone> */}
                                <input type="file" onChange={handleFileInputChange} multiple />

                            </div>
                        </div>
                    </div>

                    <div className="col-md-6">
                        <div className="card shadow mb-4">
                            <div
                                className="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                <h6 className="m-0 font-weight-bold text-primary">Variants</h6>
                            </div>
                            <div className="card-body">

                                {
                                    productVariants.map((element, index) => {
                                        return (
                                            <div className="row" key={index}>
                                                <div className="col-md-4">
                                                    <div className="form-group">
                                                        <label htmlFor="">Option</label>
                                                        <select className="form-control" defaultValue={element.option}>
                                                            {
                                                                JSON.parse(props.variants.replaceAll("'", '"')).map((variant, index) => {
                                                                    return (<option key={index}
                                                                                    value={variant.id}>{variant.title}</option>)
                                                                })
                                                            }

                                                        </select>
                                                    </div>
                                                </div>

                                                <div className="col-md-8">
                                                    <div className="form-group">
                                                        {
                                                            productVariants.length > 1
                                                                ? <label htmlFor="" className="float-right text-primary"
                                                                         style={{marginTop: "-30px"}}
                                                                         onClick={() => removeProductVariant(index)}>remove</label>
                                                                : ''
                                                        }

                                                        <section style={{marginTop: "30px"}}>
                                                            <TagsInput value={element.tags}
                                                                       style="margin-top:30px"
                                                                       onChange={(value) => handleInputTagOnChange(value, index)}/>
                                                        </section>

                                                    </div>
                                                </div>
                                            </div>
                                        )
                                    })
                                }


                            </div>
                            <div className="card-footer">
                                {productVariants.length !== 3
                                    ? <button className="btn btn-primary" onClick={handleAddClick}>Add another
                                        option</button>
                                    : ''
                                }

                            </div>

                            <div className="card-header text-uppercase">Preview</div>
                            <div className="card-body">
                                <div className="table-responsive">
                                    <table className="table">
                                        <thead>
                                        <tr>
                                            <td>Variant</td>
                                            <td>Price</td>
                                            <td>Stock</td>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {
                                            productVariantPrices.map((productVariantPrice, index) => {
                                                return (
                                                    <tr key={index}>
                                                        <td>{productVariantPrice.title}</td>
                                                        <td><input className="form-control" type="text"/></td>
                                                        <td><input className="form-control" type="text"/></td>
                                                    </tr>
                                                )
                                            })
                                        }
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button type="submit"  className="btn btn-lg btn-primary">Save</button>
                <button type="button" className="btn btn-secondary btn-lg">Cancel</button>
                </form>

               
            </section>
        </div>
    );
};

export default CreateProduct;
